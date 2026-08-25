# Repository Guidelines

## Project Structure & Module Organization

This Bookdown repository delivers a Russian-language Git course. Root-level files such as `02-01-init.Rmd` are chapters; `index.Rmd` controls their order and titles. `_common.R`, `_bookdown.yml`, and `_output.yml` hold shared rendering and theme settings. Put images in `img/` and use relative paths. `docs/` is committed output; never hand-edit its generated HTML, copied images, or `libs/`. Practice material is in `practice/`; `practice-old/` is archival. `renv.lock` pins R package versions.

## Purpose & Audience

This is an onboarding course for the Institute of Bioinformatics programme «Биостатистика и анализ медицинских данных». Before day one, every cohort member should have a working environment and basic R/tidyverse knowledge. It is not a general-audience textbook. Prioritize actionable setup, short checks, and likely blockers; omit material that does not help students arrive ready. Success means fewer students arrive unprepared or become blocked in class.

## Build, Test, and Development Commands

- `R -e 'renv::restore()'` installs the package versions recorded in `renv.lock` (run after cloning or changing the lockfile).
- `make build` runs `bookdown::render_book(output_dir="docs")` and regenerates the published site.
- `make dev` serves the Bookdown site locally and rebuilds it while editing.
- `R -e 'rmarkdown::render("practice/workshop_notebook.Rmd")'` renders an individual practice notebook when that material changes.

There is no separate test suite. A clean successful render is the primary check; inspect the changed pages in `docs/` and verify chapter links, code blocks, citations, and image paths before committing.

## Writing, Code Style & Naming

Follow the existing R Markdown style: Russian prose, concise headings, and runnable fenced R or shell examples. For reader-facing text, consult [authors-voice.md](/Users/ydb/Work/BioInf/git-course/authors-voice.md) and apply [@ru-text](plugin://ru-text@openai-curated-remote). Use two-space R indentation and preserve `_common.R` chunk defaults. Name chapters `NN-NN-topic.Rmd` (for example, `05-04-hooks.Rmd`) and images with lowercase hyphenated names, e.g. `img/05-04-hook-settings.png`. Prefer relative paths; do not commit `.RData`, `.Rhistory`, or `.Rproj.user`.

## Commit & Pull Request Guidelines

Recent history uses short, imperative Russian messages, e.g. `Добавил рендеринг Rmd` or `Поправил формулировки`. Keep commits focused; use merge commits only for merges. Pull requests should explain the instructional change, list affected chapters/practice files, and include rendered `docs/` updates for source changes. Add before/after screenshots for visual changes and link the relevant issue or lesson request when available.
