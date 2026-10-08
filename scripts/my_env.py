import sys
import subprocess
from pathlib import Path

python_version = sys.version.split()[0]

try:
    quarto_version = subprocess.run(
        ["quarto", "--version"], capture_output=True, text=True, check=True
    ).stdout.strip()
except (OSError, subprocess.CalledProcessError):
    quarto_version = "unknown"

Path("_metadata.yml").write_text(
    "metadata:\n"
    f'  python-version: "{python_version}"\n'
    f'  quarto-version: "{quarto_version}"\n',
    encoding="utf-8",
)