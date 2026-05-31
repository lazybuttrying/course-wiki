#!/usr/bin/env bash
# bootstrap.sh — instantiate a new course wiki from this harness in one command.
#
#   ./bootstrap.sh -c "Causal Inference" -v ../class/causality/wiki/Causality-wiki \
#                  -s "../../course_files_export/" -u lecture -m on -e on
#
# Copies template-vault → <vault>, generates CLAUDE.md from CLAUDE.template.md
# (strips the BOOTSTRAP block), substitutes {{placeholders}} in the meta files,
# stamps today's date, and records settings in <vault>/wiki.config.yml.
# Page templates in _templates/ are copied verbatim (not substituted).
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COURSE=""; VAULT=""; SRC=""; UNIT="chapter"; MATH="on"; TERMS="on"; TYPES="PDF · slides · notes"

usage() { sed -n '2,12p' "$0"; exit 1; }
while getopts "c:v:s:u:m:e:t:h" o; do case "$o" in
  c) COURSE="$OPTARG";; v) VAULT="$OPTARG";; s) SRC="$OPTARG";;
  u) UNIT="$OPTARG";; m) MATH="$OPTARG";; e) TERMS="$OPTARG";; t) TYPES="$OPTARG";;
  *) usage;; esac; done
[ -z "$COURSE" ] || [ -z "$VAULT" ] || [ -z "$SRC" ] && { echo "missing -c/-v/-s"; usage; }
[ -e "$VAULT" ] && { echo "ERROR: '$VAULT' already exists — aborting."; exit 1; }

VAULTNAME="$(basename "$VAULT")"
TODAY="$(date +%F)"
sed_i() { sed -i.bak "$@" && rm -f "${@: -1}.bak"; }   # BSD/GNU-portable in-place

echo "→ copying skeleton to $VAULT"
mkdir -p "$(dirname "$VAULT")"
cp -R "$REPO/template-vault" "$VAULT"

echo "→ generating CLAUDE.md (strip BOOTSTRAP block + substitute)"
awk '/BOOTSTRAP:START/{f=1} /BOOTSTRAP:END/{f=0;next} !f' \
    "$REPO/CLAUDE.template.md" > "$VAULT/CLAUDE.md"

echo "→ substituting placeholders in meta files"
for f in CLAUDE.md index.md log.md Welcome.md; do
  [ -f "$VAULT/$f" ] || continue
  sed_i \
    -e "s|{{COURSE}}|$COURSE|g" \
    -e "s|{{VAULT}}|$VAULTNAME|g" \
    -e "s|{{SOURCE_DIRS}}|$SRC|g" \
    -e "s|{{SOURCE_TYPES}}|$TYPES|g" \
    -e "s|{{UNIT}}|$UNIT|g" \
    -e "s|{{KEEP_ENGLISH_TERMS}}|$TERMS|g" \
    -e "s|{{MATH}}|$MATH|g" \
    -e "s|YYYY-MM-DD|$TODAY|g" \
    "$VAULT/$f"
done

cat > "$VAULT/wiki.config.yml" <<EOF
# Settings recorded at bootstrap (scripts/humans may read this).
course: "$COURSE"
vault: "$VAULTNAME"
source_dirs: "$SRC"
source_types: "$TYPES"
unit: "$UNIT"          # chapter | week | lecture | module | paper
keep_english_terms: "$TERMS"
math: "$MATH"
created: "$TODAY"
EOF

echo
echo "✅ done: $VAULT"
echo "next:"
echo "  1) 소스를 $SRC 에 두고(immutable) 확인"
echo "  2) LLM에게: \"$VAULT/CLAUDE.md 스키마대로 <소스>를 ingest 해줘\""
echo "  3) lint:  python3 \"$REPO/scripts/lint.py\" \"$VAULT\""
