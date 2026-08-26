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
PRACTICE_SOURCES = sorted((ROOT / "practice").rglob("*.qmd")) + sorted(
    (ROOT / "practice").glob("*.patch")
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
        if "RStudio" in text or "Rstudio" in text:
            fail(f"{source.name}: осталось упоминание RStudio", failures)
        if "R Markdown" in text or "RMarkdown" in text:
            fail(f"{source.name}: осталось упоминание R Markdown", failures)
        for match in re.finditer(r"!\[([^\]]*)\]\(([^)]*)\)", text):
            alt, target = match.groups()
            if not alt.strip():
                fail(f"{source.name}: у изображения нет описания", failures)
            if target.strip():
                fail(f"{source.name}: скриншот должен иметь пустой адрес: {target}", failures)

    for source in PRACTICE_SOURCES:
        text = source.read_text(encoding="utf-8")
        relative = source.relative_to(ROOT)
        if "%>%" in text:
            fail(f"{relative}: используется %>%", failures)
        if "RStudio" in text or "Rstudio" in text:
            fail(f"{relative}: осталось упоминание RStudio", failures)
        if "R Markdown" in text or "RMarkdown" in text:
            fail(f"{relative}: осталось упоминание R Markdown", failures)
        if ".Rmd" in text:
            fail(f"{relative}: активный файл ссылается на .Rmd", failures)

    generator = (ROOT / "bin" / "create_course_project.py").read_text(encoding="utf-8")
    if "%>%" in generator:
        fail("create_course_project.py: используется %>%", failures)
    if 'read.csv("data/penguins.csv")' not in generator:
        fail("create_course_project.py: paper.qmd читает данные не из data/penguins.csv", failures)
    if "|>" not in generator:
        fail("create_course_project.py: в новом R-коде нет базовой трубы |>", failures)

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
