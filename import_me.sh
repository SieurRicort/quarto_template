#!/usr/bin/env bash
# import_me.sh - copy the template files into a new project folder.
#
# Usage: ./import_me.sh /absolute/path/to/my_project
#
# Run it from your local clone of the template. It copies from the folder
# the script lives in, so nothing is downloaded or cloned.

set -euo pipefail

# Files and folders to import (edit this list when the template changes)
FILES=(template.qmd .gitignore _quarto.yml styles.css scripts)

# Folder containing this script (follows symlinks, works from any directory)
TEMPLATE="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

usage() {
  echo "Usage: $0 /absolute/path/to/my_project"
}

if [[ $# -eq 1 && ( "$1" == "-h" || "$1" == "--help" ) ]]; then
  usage
  exit 0
fi

if [[ $# -ne 1 ]]; then
  usage >&2
  exit 1
fi

PROJECT="${1%/}"

# Absolute path required, so files cannot land in an unexpected place
if [[ "$PROJECT" != /* ]]; then
  echo "Error: use an absolute path (starting with / or ~), got '$1'" >&2
  exit 1
fi

# Check that everything in FILES exists in the template
for f in "${FILES[@]}"; do
  if [[ ! -e "$TEMPLATE/$f" ]]; then
    echo "Error: '$f' not found in $TEMPLATE" >&2
    exit 1
  fi
done

# Never overwrite: stop if any file already exists in the project
conflicts=()
for f in "${FILES[@]}"; do
  if [[ -e "$PROJECT/$f" ]]; then
    conflicts+=("$f")
  fi
done
if (( ${#conflicts[@]} > 0 )); then
  echo "Error: these already exist in $PROJECT, nothing was copied:" >&2
  printf '  %s\n' "${conflicts[@]}" >&2
  exit 1
fi

mkdir -p "$PROJECT"
(cd "$TEMPLATE" && cp -r "${FILES[@]}" "$PROJECT"/)

echo "Imported into $PROJECT:"
printf '  %s\n' "${FILES[@]}"
echo
echo "Next: cd \"$PROJECT\" and copy template.qmd to a new name,"
echo "      e.g. cp template.qmd my_analysis.qmd"