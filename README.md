# Quarto Analysis Template

A reusable [Quarto](https://quarto.org) template for documenting bioinformatics analyses as a single, shareable HTML report. Each report follows the same structure (goal, script, results, personal notes) and ends with an automatic **Environment** table recording the versions used.

## Repository structure

```
.
├── LICENSE # Licence for reuse
├── README.md # This file
├── .gitignore # Variety of files not pushed in your git
├── _quarto.yml # Quarto project settings (output format, theme, options)
├── html_output
│ └── template.html # Example of the rendered report
├── import_me.sh # Imports the template into a new project
├── scripts
│ ├── display_results.py # Displays command then its output below with %%show
│ └── my_env.py # Builds the Environment table (last code cell of the report)
├── setup_conda_env.sh # Setup conda env for the project
├── styles.css # Custom styling for the HTML output
├── template.qmd # The report template
└── .vscode
└── quarto.code-snippets # VS Code snippets
```

## Requirements

- **Quarto CLI** ([install](https://quarto.org/docs/get-started/)), tested with 1.10. Check with `quarto --version`
- **Python 3.10+** with **Jupyter** (`jupyter`, `ipykernel`) and a kernel named `python3`. Miniconda is recommended
- **VS Code** (optional) with the **Quarto**, **Python** and **Jupyter** extensions
- **Command-line tools** you want reported in the Environment table (for example `samtools`), on your `PATH`

Notes:

- The Quarto VS Code extension does **not** include Quarto itself. Install the CLI separately and restart VS Code.
- On Windows with WSL2, install Quarto *inside* WSL and use the VS Code **WSL** extension, so editor, Python and Quarto share the same environment.

## Getting the template

Clone this repository **once** somewhere on your machine, create your project directory and execute the script `import_me.sh`.

```bash
git clone https://github.com/SieurRicort/quarto_template ~/quarto_template        # Once
mkdir -p ~/projects/my_project   # Make sure you create the directory you want to work in
cd ~/projects/my_project   # Go to your project directory so you can execute the script that will import everything you need
/true/path/to/import_me.sh   # Will import everything needed for you to start working on the template in your working project
```

`import_me.sh` refuses to run inside the template directory itself and refuses to overwrite any file or folder that already exists in your project (it lists the conflicts and copies nothing). Re-running it in a project that already has the template files is a safe way to check what would conflict, but it won't update anything for you — see below.

To pick up template updates, run `git pull` in `~/quarto_template`. Existing projects are **not** updated automatically, which is intentional: an old report keeps the template version it was written with. Releases are tagged (`v0.1.0`, `v0.2.0`, ...), so you can note which version a project started from.

Avoid cloning the template inside every project: it drags along the template's Git history and remote.

## Setting up the conda environment

Each project should get its own environment, never `base` (which changes over time and breaks reproducibility between projects).

### Automated: `setup_conda_env.sh`

The imported `setup_conda_env.sh` creates the environment and installs the Jupyter stack needed for Quarto to find a kernel, plus whatever extra packages you list:

```bash
#!/usr/bin/env bash
name="myproject"    # change for a new name every time you want a fresh env
ver="3.12"           # bioinformatics -> python version should be 3.12
base_modules=(pip ipython ipykernel jupyter)
...
more_modules=(pandas numpy biopython)   # edit this list
```

Edit `name` and `more_modules` for your project, then run:

```bash
bash setup_conda_env.sh
```

It's idempotent on the environment itself (skips creation if `name` already exists) but always re-runs the `conda install` for `more_modules`, so you can rerun it later to add packages without recreating the environment.

### Manual

```bash
conda create -n myproject python=3.12 jupyter
conda activate myproject
conda install -c bioconda -c conda-forge samtools bwa   # optional command-line tools
```

### Either way, check it's picked up

```bash
conda activate myproject
quarto check
quarto check jupyter
```

**In VS Code, select the interpreter with `Ctrl+Shift+P` → *Python: Select Interpreter* → pick `myproject`.**

## Usage

1. Copy `template.qmd` to a new name (for example `my_analysis.qmd`).
2. Fill in the header: title, description, author, date, and the `metadata` block (`analysis-type`, `status`).
3. Write the analysis in the provided sections. To add another analysis to the same report, insert it with the `qblockpy` snippet (see [Snippets](#snippets)).
4. Edit the lists at the end of the Environment cell:

```python
   tools = ["samtools", "bwa"]
   packages = ["pandas", "numpy"]
```

5. Activate your environment and render:

```bash
   conda activate myproject
   quarto render my_analysis.qmd
```

The result is a single HTML file written to `html_output` (set in `_quarto.yml`: `project -> output-dir`).

## The Environment table

Generated by `scripts/my_env.py`. It reports Python, Quarto, the Linux distro, the active conda environment, and the versions of the tools and packages you list. Missing items never raise an error (they show `not found` or `not installed`).

If a tool shows `version not detected`, add its version command to `TOOL_CMDS` at the top of `scripts/my_env.py`:

```python
TOOL_CMDS = {
    "bwa": ["bwa"],
    "mytool": ["mytool", "--about"],   # add entries as needed
}
```

For full reproducibility, also export the environment next to your report:

```bash
conda env export --from-history > environment.yml
```

## Snippets

Defined in `.vscode/quarto.code-snippets`, scoped to Quarto files. Type the prefix and press `Tab`.

- **`qblockpy`** — inserts a full analysis block: goal, `### Script`, `### Results` (pre-wired with `%%show`), and a collapsible `### Personal notes` callout. Tab through the placeholders to fill title, goal, code and command.
- **`py_display_results`** — inserts the setup cell that locates `scripts/display_results.py` from anywhere in the project tree and registers the `%%show` magic. The template already includes one at the top; use this snippet only if you add a second `.qmd` file that also needs `%%show`, or if you removed the original setup cell.

### Adding or editing snippets

1. In VS Code: `Ctrl+Shift+P` → *Snippets: Configure Snippets* → `quarto` (creates or opens `.vscode/quarto.code-snippets`).
2. Follow the existing JSON structure: a name, `"prefix"`, `"scope": "quarto"`, `"description"`, and a `"body"` array of lines. Use `${n:placeholder}` for tab stops and `$0` for the final cursor position.
3. Commit the updated `quarto.code-snippets` to the **template repo** (not just the project) if you want it available in future projects — `import_me.sh` only copies what exists in the template at clone time.

## Tips and tricks

- **Live preview:** `quarto preview my_analysis.qmd`, or `Ctrl+Shift+K` in VS Code
- **Run code interactively** in VS Code: `Ctrl+Enter` (line/selection), `Ctrl+Shift+Enter` (cell)
- **Cell options** (`#| echo: false`, `#| code-fold: true`, `#| fig-cap`, ...): see the [cell options reference](https://quarto.org/docs/reference/cells/cells-jupyter.html)
- **Skip slow re-computation** with [`freeze: auto`](https://quarto.org/docs/projects/code-execution.html#freeze) under `execute:` in `_quarto.yml`
- **Styling:** edit `styles.css`, use your browser's *Inspect* tool to find the class of an element, or switch `theme:` in `_quarto.yml` to another [Bootswatch theme](https://quarto.org/docs/output-formats/html-themes.html)
- **Callouts, tabsets and wide layouts:** see the Quarto docs on [callouts](https://quarto.org/docs/authoring/callouts.html), [tabsets](https://quarto.org/docs/interactive/layout.html#tabsets) and [article layout](https://quarto.org/docs/authoring/article-layout.html)
- **Shell commands** from a Python cell: prefix with `!` or start the cell with `%%bash`

## Troubleshooting

- **`Permission denied` running `import_me.sh` or `setup_conda_env.sh`**: scripts aren't executable after cloning. `chmod +x import_me.sh setup_conda_env.sh`, or run them as `bash import_me.sh` without chmod.
  
- **`quarto: command not found`**: Quarto CLI isn't installed, or isn't installed in the system your terminal actually runs in. The VS Code Quarto extension does **not** bundle Quarto — install the CLI separately from [quarto.org](https://quarto.org/docs/get-started/), then restart the terminal (and VS Code, since it caches `PATH` at launch). On WSL2, install it *inside* WSL, not on the Windows side.
  
- **Wrong Python used when rendering**: Quarto picks whatever `python3`/`jupyter` is first on `PATH` at render time — this is independent of whichever interpreter is selected in the VS Code editor. Always `conda activate myproject` in the same terminal before `quarto render`. If rendering via the VS Code Quarto extension's preview/render button, also check `Ctrl+Shift+P` → *Python: Select Interpreter* matches. Run `quarto check jupyter` to see which kernel Quarto actually found if unsure.
  
- **`ModuleNotFoundError: my_env` or `display_results`**: render from the project root, or adjust the `sys.path.insert` / `candidates` logic at the top of the relevant cell if your `.qmd` lives in a subfolder.

## Before sharing a report

Reports are rendered with `echo: true` and `embed-resources: true`, so the HTML contains your full code and outputs. Open the file and check that it does not expose absolute paths with your username, sample IDs or other sensitive data, tracebacks, or credentials.

## License

MIT License, see the [LICENSE](https://github.com/SieurRicort/quarto_template/blob/main/LICENSE) file.
