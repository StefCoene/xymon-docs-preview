# xymon-docs-preview

Unofficial preview of a central documentation site for [Xymon](https://github.com/xymon-monitoring/xymon).

**Live:** https://stefcoene.github.io/xymon-docs-preview/

The home page is a Xymon-style status grid: topics × documentation types, coloured by how current
each source is. Content is pulled from the `xymon`, `xymon-wiki` and `xymon-plugins` repositories on
every build (see `scripts/fetch-sources.sh`); the grid is defined in `matrix.yml` and rendered by
`hooks/xymon_matrix.py`.

## Build locally

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
scripts/fetch-sources.sh
mkdocs serve
```
