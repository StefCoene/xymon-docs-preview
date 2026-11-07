#!/usr/bin/env bash
# Pull documentation from the xymon-monitoring repositories into docs/.
# Everything written here is generated: it is git-ignored and rebuilt on every CI run.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
SRC="$ROOT/.sources"
DOCS="$ROOT/docs"
ORG="https://github.com/xymon-monitoring"
STABLE_REF="${STABLE_REF:-rel-4.3.31}"

rm -rf "$SRC" "$DOCS/manual" "$DOCS/guides" "$DOCS/project" "$DOCS/clients/windows-powershell" "$DOCS/plugins" \
  "$DOCS/contributing" "$DOCS/development"
mkdir -p "$SRC"

# Blob-less clones keep full history (for last-changed dates) without downloading every file.
clone() {  # clone <repo> <dir> [ref]
  git clone --quiet --filter=blob:none --no-checkout "$ORG/$1.git" "$SRC/$2"
  git -C "$SRC/$2" checkout --quiet "${3:-HEAD}"
}
clone xymon        xymon
clone xymon        xymon-stable "$STABLE_REF"
clone xymon-wiki   xymon-wiki
clone xymon-plugins xymon-plugins

# dates.json maps a path under docs/ to the date its source last changed.
DATES="$SRC/dates.tsv"
: > "$DATES"
record() {  # record <repo-dir> <path-in-repo> <path-under-docs>
  printf '%s\t%s\n' "$3" "$(git -C "$SRC/$1" log -1 --format=%cs -- "$2")" >> "$DATES"
}

copy_manual() {  # copy_manual <repo-dir> <version>
  local from="$SRC/$1/docs" to="$DOCS/manual/$2"
  mkdir -p "$to"
  (cd "$from" && find . -type f ! -name Makefile ! -name TODO -print) | while read -r f; do
    f=${f#./}
    dest=${f%.DIST}
    mkdir -p "$to/$(dirname "$dest")"
    cp "$from/$f" "$to/$dest"
    record "$1" "docs/$f" "manual/$2/$dest"
  done
}
copy_manual xymon        dev
copy_manual xymon-stable 4.3

copy_md() {  # copy_md <repo-dir> <path-in-repo> <path-under-docs>
  mkdir -p "$DOCS/$(dirname "$3")"
  cp "$SRC/$1/$2" "$DOCS/$3"
  record "$1" "$2" "$3"
}
# xymon-wiki: every page, in the same layout. Only about/ moves, to project/, because this site's
# about.md describes the site itself. The navigation comes from the wiki's own mkdocs.yml (see the hook).
(cd "$SRC/xymon-wiki/docs" && git ls-files '*.md') | while read -r f; do
  [ "$f" = index.md ] && continue
  copy_md xymon-wiki "docs/$f" "$(printf '%s' "$f" | sed 's#^about/#project/#')"
done

# xymon-plugins: keep the repository layout so the READMEs' relative links keep working.
(cd "$SRC/xymon-plugins" && git ls-files '*.md') | while read -r f; do
  case "$f" in AGENTS.md|CLAUDE.md|CONTRIBUTING.md) continue ;; esac
  copy_md xymon-plugins "$f" "plugins/$f"
done

python3 -I - "$DATES" "$SRC/dates.json" <<'EOF'
import json, sys
rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1]) if l.strip()]
json.dump({p: d for p, d in rows}, open(sys.argv[2], "w"), indent=1, sort_keys=True)
EOF

echo "Fetched: $(wc -l < "$DATES") files (stable = $STABLE_REF)"
