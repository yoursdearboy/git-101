#!/usr/bin/env python3
"""Create reproducible checkpoints for the Positron Git course."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "course-project" / "starter"
OUTPUTS = ROOT / "course-project" / "outputs"
MANIFEST = ROOT / "course-project" / "starter-manifest.json"

LOCAL_STATES = (
    "starter",
    "baseline",
    "paper",
    "histogram",
    "boxplot-branch",
    "dirty-main",
    "conflict",
    "merged",
)
GITHUB_STATES = (
    "github-published",
    "github-pr",
    "github-merged",
    "github-webhook",
)
STATES = LOCAL_STATES + GITHUB_STATES

GIT_ENV = {
    "GIT_AUTHOR_NAME": "Участник курса",
    "GIT_AUTHOR_EMAIL": "student@example.org",
    "GIT_COMMITTER_NAME": "Участник курса",
    "GIT_COMMITTER_EMAIL": "student@example.org",
}


class CourseProjectError(RuntimeError):
    """An expected error that can be shown without a traceback."""


def run(
    args: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    command_env = os.environ.copy()
    if env:
        command_env.update(env)
    result = subprocess.run(
        args,
        cwd=cwd,
        env=command_env,
        check=False,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        if detail:
            raise CourseProjectError(f"Команда завершилась с ошибкой: {' '.join(args)}\n{detail}")
        raise CourseProjectError(f"Команда завершилась с ошибкой: {' '.join(args)}")
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_starter(path: Path) -> None:
    expected = json.loads(MANIFEST.read_text(encoding="utf-8"))
    actual_paths = sorted(
        item.relative_to(path).as_posix()
        for item in path.rglob("*")
        if item.is_file() and ".git" not in item.relative_to(path).parts
    )
    expected_paths = sorted(expected)
    if actual_paths != expected_paths:
        raise CourseProjectError("Состав стартового проекта не совпадает с манифестом")
    for relative, metadata in expected.items():
        item = path / relative
        if item.stat().st_size != metadata["size"] or sha256(item) != metadata["sha256"]:
            raise CourseProjectError(f"Стартовый файл повреждён: {relative}")


def initialize_repository(target: Path) -> None:
    initialized = run(["git", "init", "-b", "main"], cwd=target, check=False, capture=True)
    if initialized.returncode != 0:
        run(["git", "init"], cwd=target)
        run(["git", "branch", "-m", "main"], cwd=target)
    run(["git", "config", "user.name", GIT_ENV["GIT_AUTHOR_NAME"]], cwd=target)
    run(["git", "config", "user.email", GIT_ENV["GIT_AUTHOR_EMAIL"]], cwd=target)


def copy_starter(target: Path) -> None:
    if target.exists():
        raise CourseProjectError(f"Путь уже существует: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(STARTER, target, copy_function=shutil.copy2)
    try:
        validate_starter(target)
        initialize_repository(target)
    except Exception:
        shutil.rmtree(target)
        raise


def commit(target: Path, message: str, day: int) -> None:
    run(["git", "add", "-A"], cwd=target, capture=True)
    stamp = f"2026-09-{day:02d}T09:00:00+03:00"
    run(
        ["git", "commit", "-m", message],
        cwd=target,
        env={**GIT_ENV, "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp},
        capture=True,
    )


def write_paper(target: Path, version: str) -> None:
    bodies = {
        "paper": '''---
title: "Длина клюва пингвинов"
format: html
---

```{r}
data <- read.csv("data/penguins.csv")
x <- data$bill_len |> na.omit()
x
```
''',
        "histogram": '''---
title: "Длина клюва пингвинов"
format: html
---

```{r}
data <- read.csv("data/penguins.csv")
x <- data$bill_len |> na.omit()

png("out/penguins-hist.png")
hist(x, breaks = seq(30, 60, 2))
dev.off()
```
''',
        "histogram-labelled": '''---
title: "Длина клюва пингвинов"
format: html
---

```{r}
data <- read.csv("data/penguins.csv")
x <- data$bill_len |> na.omit()

png("out/penguins-hist.png")
hist(x, breaks = seq(30, 60, 2), xlab = "Bill length, mm")
dev.off()
```
''',
        "boxplot": '''---
title: "Длина клюва пингвинов"
format: html
---

```{r}
data <- read.csv("data/penguins.csv")
x <- data$bill_len |> na.omit()

png("out/penguins-boxplot.png")
boxplot(x)
dev.off()
```
''',
        "boxplot-labelled": '''---
title: "Длина клюва пингвинов"
format: html
---

```{r}
data <- read.csv("data/penguins.csv")
x <- data$bill_len |> na.omit()

png("out/penguins-boxplot.png")
boxplot(x, ylab = "Bill length, mm")
dev.off()
```
''',
        "by-sex": '''---
title: "Длина клюва пингвинов"
format: html
---

```{r}
data <- read.csv("data/penguins.csv")
x <- data$bill_len
g <- data$sex

png("out/penguins-boxplot.png")
boxplot(x ~ g, xlab = "Sex", ylab = "Bill length, mm")
dev.off()
```
''',
    }
    (target / "paper.qmd").write_text(bodies[version], encoding="utf-8")


def copy_output(target: Path, source: str, destination: str) -> None:
    output = target / "out" / destination
    output.parent.mkdir(exist_ok=True)
    shutil.copy2(OUTPUTS / source, output)


def make_baseline(target: Path) -> None:
    commit(target, "Зафиксировал результат курса R", 1)


def make_paper(target: Path) -> None:
    make_baseline(target)
    write_paper(target, "paper")
    commit(target, "Добавил импорт данных в paper.qmd", 2)


def make_histogram(target: Path) -> None:
    make_paper(target)
    write_paper(target, "histogram")
    copy_output(target, "penguins-hist.png", "penguins-hist.png")
    commit(target, "Сохранил гистограмму длины клюва", 3)


def make_boxplot_branch(target: Path) -> None:
    make_histogram(target)
    run(["git", "switch", "-c", "boxplot"], cwd=target, capture=True)
    write_paper(target, "boxplot")
    (target / "out" / "penguins-hist.png").unlink()
    copy_output(target, "penguins-boxplot.png", "penguins-boxplot.png")
    commit(target, "Заменил гистограмму на ящик с усами", 4)


def make_dirty_main(target: Path) -> None:
    make_boxplot_branch(target)
    run(["git", "switch", "main"], cwd=target, capture=True)
    write_paper(target, "histogram-labelled")


def make_conflict(target: Path) -> None:
    make_dirty_main(target)
    commit(target, "Добавил подпись оси гистограммы", 5)
    merged = run(["git", "merge", "boxplot"], cwd=target, check=False, capture=True)
    if merged.returncode == 0:
        raise CourseProjectError("Не удалось создать учебный конфликт слияния")


def make_merged(target: Path) -> None:
    make_conflict(target)
    write_paper(target, "boxplot-labelled")
    copy_output(target, "penguins-boxplot-labelled.png", "penguins-boxplot.png")
    commit(target, "Слил ветку boxplot", 6)


def make_adjust_by_sex(target: Path) -> None:
    make_merged(target)
    run(["git", "switch", "-c", "adjust-by-sex"], cwd=target, capture=True)
    write_paper(target, "by-sex")
    copy_output(target, "penguins-boxplot-by-sex.png", "penguins-boxplot.png")
    commit(target, "Сгруппировал пингвинов по полу", 7)


def build_local_state(target: Path, state: str) -> None:
    builders = {
        "starter": lambda path: None,
        "baseline": make_baseline,
        "paper": make_paper,
        "histogram": make_histogram,
        "boxplot-branch": make_boxplot_branch,
        "dirty-main": make_dirty_main,
        "conflict": make_conflict,
        "merged": make_merged,
    }
    builders[state](target)


def ensure_gh_auth() -> None:
    if shutil.which("gh") is None:
        raise CourseProjectError("Не найден GitHub CLI (gh). Установите его и повторите запуск")
    status = run(["gh", "auth", "status", "-h", "github.com"], check=False)
    if status.returncode != 0:
        print("Откроется браузер для входа в GitHub.")
        run(["gh", "auth", "login", "--web", "-h", "github.com", "-p", "https"])
        run(["gh", "auth", "status", "-h", "github.com"])


def ensure_remote_absent(repository: str) -> None:
    existing = run(
        ["gh", "repo", "view", repository, "--json", "nameWithOwner"],
        check=False,
        capture=True,
    )
    if existing.returncode == 0:
        raise CourseProjectError(f"Репозиторий GitHub уже существует: {repository}")
    detail = (existing.stderr or existing.stdout or "").strip()
    missing_markers = ("Could not resolve to a Repository", "HTTP 404", "Not Found")
    if detail and not any(marker in detail for marker in missing_markers):
        raise CourseProjectError(f"Не удалось проверить репозиторий GitHub:\n{detail}")


def publish_repository(target: Path, repository: str, visibility: str) -> None:
    current_branch = run(
        ["git", "branch", "--show-current"], cwd=target, capture=True
    ).stdout.strip()
    if current_branch != "main":
        run(["git", "switch", "main"], cwd=target, capture=True)
    run(
        [
            "gh",
            "repo",
            "create",
            repository,
            "--source=.",
            "--remote=origin",
            "--push",
            f"--{visibility}",
        ],
        cwd=target,
    )
    run(["git", "push", "--all", "origin"], cwd=target)
    if current_branch != "main":
        run(["git", "switch", current_branch], cwd=target, capture=True)


def create_pull_request(target: Path, repository: str) -> str:
    run(["git", "push", "-u", "origin", "adjust-by-sex"], cwd=target)
    created = run(
        [
            "gh",
            "pr",
            "create",
            "--repo",
            repository,
            "--base",
            "main",
            "--head",
            "adjust-by-sex",
            "--title",
            "Сгруппировал пингвинов по полу",
            "--body",
            "Ящик с усами теперь показывает распределение длины клюва отдельно для каждого пола.",
        ],
        cwd=target,
        capture=True,
    )
    return created.stdout.strip()


def add_webhook(repository: str, url: str, secret: str | None) -> None:
    args = [
        "gh",
        "api",
        "--method",
        "POST",
        f"repos/{repository}/hooks",
        "-f",
        "name=web",
        "-F",
        "active=true",
        "-f",
        f"config[url]={url}",
        "-f",
        "config[content_type]=json",
        "-f",
        "events[]=pull_request",
    ]
    if secret:
        args.extend(["-f", f"config[secret]={secret}"])
    run(args)


def build_github_state(
    target: Path,
    state: str,
    repository: str,
    visibility: str,
    webhook_url: str | None,
    webhook_secret: str | None,
) -> None:
    if state == "github-published":
        make_merged(target)
        publish_repository(target, repository, visibility)
        return

    make_adjust_by_sex(target)
    publish_repository(target, repository, visibility)

    if state == "github-webhook":
        if not webhook_url:
            raise CourseProjectError("Для github-webhook нужен параметр --webhook-url")
        add_webhook(repository, webhook_url, webhook_secret)

    pull_request = create_pull_request(target, repository)
    print(f"Pull request: {pull_request}")

    if state == "github-merged":
        run(
            ["gh", "pr", "merge", pull_request, "--repo", repository, "--merge", "--delete-branch"],
            cwd=target,
        )
        run(["git", "switch", "main"], cwd=target)
        run(["git", "pull", "--ff-only", "origin", "main"], cwd=target)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Создать проект для выбранной контрольной точки курса Git",
    )
    parser.add_argument("target", type=Path, help="новая папка проекта")
    parser.add_argument("--state", choices=STATES, default="starter")
    parser.add_argument("--repo", help="репозиторий GitHub в формате OWNER/NAME")
    parser.add_argument("--visibility", choices=("private", "public"), default="private")
    parser.add_argument("--webhook-url")
    parser.add_argument("--webhook-secret")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target = args.target.expanduser().resolve()

    try:
        if target.exists():
            raise CourseProjectError(f"Путь уже существует: {target}")

        if args.state in GITHUB_STATES:
            if not args.repo or args.repo.count("/") != 1:
                raise CourseProjectError("Для GitHub-состояния укажите --repo OWNER/NAME")
            if args.state == "github-webhook" and not args.webhook_url:
                raise CourseProjectError("Для github-webhook нужен параметр --webhook-url")
            ensure_gh_auth()
            ensure_remote_absent(args.repo)

        copy_starter(target)
        if args.state in LOCAL_STATES:
            build_local_state(target, args.state)
        else:
            build_github_state(
                target,
                args.state,
                args.repo,
                args.visibility,
                args.webhook_url,
                args.webhook_secret,
            )
    except CourseProjectError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    print(f"Создано состояние {args.state}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
