import io
from uuid import uuid4
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, lambdify
from app.utils.vercel_blob import upload_png


async def graphic_generator(expr: str, diff_var: str) -> str:
    """Generate a graph in memory, upload it, and return its public Blob URL.

    Args:
        expr: Mathematical expression to plot.
        diff_var: Variable used as the graph's independent axis.

    Returns:
        The complete public Vercel Blob URL for the generated PNG.

    Raises:
        VercelBlobError: If the network upload fails or returns an invalid result.
        Exception: Propagates expression parsing and Matplotlib plotting errors.

    The PNG is never written to disk. The function performs network I/O and
    closes both its Matplotlib figure and in-memory buffer on every path.
    """
    x_vals = np.linspace(-50, 50, 100)

    x = symbols(diff_var)
    f = lambdify(x, sympify(expr), "numpy")
    y_vals = f(x_vals)

    if np.isscalar(y_vals):
        y_vals = np.full_like(x_vals, y_vals)

    figure = plt.figure()
    buffer = io.BytesIO()
    try:
        plt.plot(x_vals, y_vals, label=expr)
        plt.legend()
        figure.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
        png_data = buffer.getvalue()
        return await upload_png(png_data, f"graphs/{uuid4()}.png")
    finally:
        plt.close(figure)
        buffer.close()
