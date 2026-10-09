"""Cell magic %%show: display each statement of a cell followed by its result.

Usage in a .qmd file:

    ```{python}
    #| echo: false
    import sys
    sys.path.insert(0, "scripts")
    import results          # registers the %%show magic
    ```

    ```{python}
    #| echo: false
    %%show
    count
    count_above(nums, limit)
    ```
"""
import ast

from IPython import get_ipython
from IPython.core.magic import register_cell_magic
from IPython.display import display

# Simple values are printed as text (same look as Jupyter) so that the whole
# cell stays in one output block. Anything else (DataFrame, figure, ...) is
# displayed with its rich representation.
_SIMPLE = (int, float, complex, bool, str, bytes, list, tuple, dict, set, frozenset)


@register_cell_magic
def show(line, cell):
    ns = get_ipython().user_ns
    for node in ast.parse(cell).body:
        lines = ast.get_source_segment(cell, node).splitlines()
        print("> " + lines[0])
        for extra in lines[1:]:
            print("... " + extra)
        if isinstance(node, ast.Expr):
            out = eval(compile(ast.Expression(node.value), "<show>", "eval"), ns)
            if out is None:
                continue
            if isinstance(out, _SIMPLE):
                print(repr(out))
            else:
                display(out)
        else:
            exec(compile(ast.Module([node], type_ignores=[]), "<show>", "exec"), ns)