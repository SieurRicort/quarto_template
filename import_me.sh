#!/usr/bin/env bash
# import_me.sh - import template files into the current directory.
#
# Usage:
#   cd /path/to/my_project
#   /path/to/quarto_template/import_me.sh

set -Eeuo pipefail

FILES=(
  template.qmd
  .gitignore
  _quarto.yml
  styles.css
  scripts
)

# Resolve the folder containing this script
TEMPLATE="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

# Use the directory from which the script was launched
PROJECT="$(pwd -P)"

error() {
  printf 'Error: %s\n' "$1" >&2
  exit 1
}

# Check that all template items exist
for f in "${FILES[@]}"; do
  [[ -e "$TEMPLATE/$f" ]] ||
    error "Template item not found: $TEMPLATE/$f"
done

# Prevent importing the template into itself
[[ "$PROJECT" != "$TEMPLATE" ]] ||
  error "You are inside the template directory. Run this from your new project directory."

# Refuse to overwrite existing items
conflicts=()

for f in "${FILES[@]}"; do
  [[ ! -e "$PROJECT/$f" ]] || conflicts+=("$f")
done

if (( ${#conflicts[@]} > 0 )); then
  printf 'Error: these items already exist in %s:\n' "$PROJECT" >&2
  printf '  %s\n' "${conflicts[@]}" >&2
  printf 'Nothing was copied. Rename or remove the conflicting items first.\n' >&2
  exit 1
fi

# Copy template files into the current directory
cp -r -- "${FILES[@]/#/$TEMPLATE/}" "$PROJECT/"

printf 'Template imported successfully into:\n  %s\n\n' "$PROJECT"
printf 'Imported items:\n'
printf '  %s\n' "${FILES[@]}"

cat <<'EOF'

Next steps:
  1. Copy template.qmd to your analysis filename:
       cp template.qmd my_analysis.qmd
  2. Open the project in VS Code.
  3. Render the document with Quarto.
EOF