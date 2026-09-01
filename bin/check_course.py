#!/usr/bin/env python3
"""Static checks for the reader-facing course sources."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SOURCES = sorted(ROOT.glob("*.Rmd"))
PRACTICE_MIGRATED = (ROOT / "practice" / "workshop_notebook.qmd").exists()
PRACTICE_SOURCES = (
    sorted((ROOT / "practice").rglob("*.qmd"))
    + sorted((ROOT / "practice").glob("*.patch"))
    if PRACTICE_MIGRATED
    else []
)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.links.append(href)


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def main() -> int:
    failures: list[str] = []
    for source in SOURCES:
        text = source.read_text(encoding="utf-8")
        if "%>%" in text:
            fail(f"{source.name}: используется %>%", failures)
        if "Rstudio" in text:
            fail(f"{source.name}: название RStudio написано с ошибкой", failures)
        if "R Markdown" in text or "RMarkdown" in text:
            fail(f"{source.name}: осталось упоминание R Markdown", failures)
        for match in re.finditer(r"!\[([^\]]*)\]\(([^)]*)\)", text):
            alt, target = match.groups()
            if not alt.strip() and not target.strip():
                fail(f"{source.name}: пустая ссылка на изображение", failures)
            if target.strip():
                image_path = (source.parent / unquote(target.strip())).resolve()
                if not image_path.exists():
                    fail(f"{source.name}: не найдено изображение {target}", failures)

    for source in PRACTICE_SOURCES:
        text = source.read_text(encoding="utf-8")
        relative = source.relative_to(ROOT)
        if "%>%" in text:
            fail(f"{relative}: используется %>%", failures)
        if "Rstudio" in text:
            fail(f"{relative}: название RStudio написано с ошибкой", failures)
        if "R Markdown" in text or "RMarkdown" in text:
            fail(f"{relative}: осталось упоминание R Markdown", failures)
        if ".Rmd" in text:
            fail(f"{relative}: активный файл ссылается на .Rmd", failures)

    generator = (ROOT / "bin" / "create_course_project.py").read_text(encoding="utf-8")
    if "%>%" in generator:
        fail("create_course_project.py: используется %>%", failures)
    if 'read.csv("data/penguins.csv")' not in generator:
        fail("create_course_project.py: paper.qmd читает данные не из data/penguins.csv", failures)
    if "mean(data$bill_len)" not in generator:
        fail("create_course_project.py: состояние paper не вычисляет среднюю длину клюва", failures)
    if "embed-resources: true" not in generator:
        fail("create_course_project.py: HTML-отчёт не встраивает ресурсы", failures)
    if 'write_html_report(target, "penguins-hist.png")' not in generator:
        fail("create_course_project.py: состояние histogram не создаёт paper.html", failures)
    if 'write_paper(target, "visualization")' not in generator:
        fail("create_course_project.py: нет состояния с тремя вариантами гистограммы", failures)
    if 'write_html_report(target, "penguins-boxplot.png")' not in generator:
        fail("create_course_project.py: ветка boxplot не обновляет paper.html", failures)
    if "png(" in generator:
        fail("create_course_project.py: paper.qmd сохраняет отдельный PNG", failures)

    docs = ROOT / "docs"
    for page in sorted(docs.glob("*.html")):
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for href in parser.links:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (page.parent / unquote(parsed.path)).resolve()
            if not target.exists():
                fail(f"{page.relative_to(ROOT)}: не найдена ссылка {href}", failures)

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"Проверено файлов курса и практики: {len(SOURCES) + len(PRACTICE_SOURCES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
