#!/usr/bin/env bash
set -e

# Variables
name="myproject"    # Change for a new name every time you want a fresh env. Please never use a space between names.
ver="3.12"    # Bioinformatics = python version should be 3.12
base_modules=(pip ipython ipykernel jupyter)

# Fresh install with base_modules needed to render on quarto
if conda env list | awk '{print $1}' | grep -qx "$name"; then
    echo "Env '$name' already exists, skipping creation."
else
    conda create -y -n "$name" -c conda-forge --override-channels python="$ver" "${base_modules[@]}"
fi

# Additional modules needed for specific analysis
more_modules=(pandas numpy biopython) # Edit this list. Keep the same format
conda install -y -n "$name" -c conda-forge --override-channels "${more_modules[@]}"