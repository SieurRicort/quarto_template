"""Environment summary table for Quarto reports.

Usage in a .qmd cell:

    from env_info import environment_table
    environment_table(tools=["samtools"], packages=["pandas"])

Nothing here raises on missing tools, packages or Quarto: failures fall
back to "not found", "not installed" or "unknown".
"""

import os
import platform
import shutil
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version

from IPython.display import Markdown

# Tools that need a non-standard command to print their version.
# Add entries as needed, e.g. {"mytool": ["mytool", "--about"]}
TOOL_CMDS = {
    "bwa": ["bwa"],
}


def quarto_version():
    try:
        return subprocess.run(
            ["quarto", "--version"],
            capture_output=True, text=True, check=True,
            stdin=subprocess.DEVNULL,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def os_info():
    system = platform.system()
    if system == "Linux":
        try:
            info = platform.freedesktop_os_release()
            distro = info.get("PRETTY_NAME", info.get("NAME", "Linux"))
        except (OSError, AttributeError):
            distro = "Linux (distro unknown)"
        if "microsoft" in platform.release().lower():
            distro += " (WSL2)"
        return distro
    if system == "Darwin":
        return f"macOS {platform.mac_ver()[0]}"
    return f"{system} {platform.release()}"


def pkg_version(pkg):
    try:
        return version(pkg)
    except PackageNotFoundError:
        return "not installed"


def tool_version(tool):
    if shutil.which(tool) is None:
        return "not found"
    cmds = (
        [TOOL_CMDS[tool]]
        if tool in TOOL_CMDS
        else [[tool, f] for f in ("--version", "-version", "version", "-v")]
    )
    for cmd in cmds:
        try:
            r = subprocess.run(
                cmd, capture_output=True, text=True, timeout=10,
                stdin=subprocess.DEVNULL,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        lines = [
            l.strip()
            for l in (r.stdout + "\n" + r.stderr).splitlines()
            if l.strip()
        ]
        for l in lines:
            if "version" in l.lower():
                return l
        if r.returncode == 0 and lines:
            return lines[0]
    return "version not detected"


def environment_table(tools=(), packages=()):
    """Return a Markdown table of the environment.

    tools:    command-line tools to report (e.g. ["samtools", "bwa"])
    packages: Python packages to report (e.g. ["pandas", "numpy"])
    """
    rows = [
        ("Python", sys.version.split()[0]),
        ("Quarto", quarto_version()),
        ("OS", os_info()),
    ]
    if os.environ.get("CONDA_DEFAULT_ENV"):
        rows.append(("Conda env", os.environ["CONDA_DEFAULT_ENV"]))
    rows += [(p, pkg_version(p)) for p in packages]
    rows += [(t, tool_version(t)) for t in tools]

    table = "| Component | Version |\n|---|---|\n" + "\n".join(
        f"| {a} | {b.replace('|', '/')} |" for a, b in rows
    )
    return Markdown(table)