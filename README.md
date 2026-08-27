# SSG-py

A small, dependency-free **static site generator** built in Python. It converts Markdown files into HTML and copies static assets (CSS, images) alongside them.

**Demo:** [**Metal Gear Catalog**](https://sFRHN.github.io/SSG-Py/)

## Layout

```
content/     Markdown source pages
static/      CSS, images, assets (copied verbatim)
src/ssg/     Generator source
tests/       Unit tests
docs/        Generated output (served by GitHub Pages)
```

## Build & run

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
./build.sh              # build site into docs/ (base path /SSG-Py/)
./main.sh               # local preview at http://localhost:8888
./test.sh               # run tests
```

Or manually: `uv run python main.py "/SSG-Py/"`

## Deploy

Build with `./build.sh`, commit the `docs/` output, and push to `main` — GitHub Pages serves it at `https://<user>.github.io/<repo>/`.
