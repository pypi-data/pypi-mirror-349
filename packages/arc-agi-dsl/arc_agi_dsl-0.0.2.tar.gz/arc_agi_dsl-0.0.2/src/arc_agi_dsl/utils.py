import sys
from IPython.display import display, HTML
from arc_agi_core import Grid, Layout
from functools import wraps
from numpy.typing import NDArray


def transformation(f: NDArray) -> NDArray:
    @wraps(f)
    def wrapper(grid: Grid) -> Grid:
        return Grid(f(grid._array))

    return wrapper


def is_running_in_ipython():
    """Detects whether we are in an IPython (Jupyter) environment."""
    try:
        shell = get_ipython().__class__.__name__  # noqa: F821
        return shell in ("ZMQInteractiveShell", "TerminalInteractiveShell")
    except NameError:
        return False


def apply_transformations(grid, transformations, show_trace=False):
    trace = [("Original", grid)]

    for transformation in transformations:
        grid = transformation(grid)
        trace.append((transformation.__name__, grid))

    if not show_trace:
        return grid

    if is_running_in_ipython():
        # Jupyter: display rich HTML
        parts = []
        for i, (label, g) in enumerate(trace):
            if i > 0:
                parts.append(
                    f'<div style="text-align:center;margin:0 1rem;text-wrap:nowrap">- {label} →</div>'
                )
            parts.append(g._repr_html_())
        html = f'<div style="display:flex;align-items:center;gap:10px;">{"".join(parts)}</div>'
        display(HTML(html))

    else:
        # Terminal: use Layout class with text representation
        layout_elements = []
        for i, (label, g) in enumerate(trace):
            if i > 0:
                layout_elements.append(f" - {label} → ")
            layout_elements.append(g)
        print(Layout(*layout_elements, direction="horizontal", align="center"))

    return grid
