import io
from uuid import uuid4
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, lambdify
from app.utils.vercel_blob import upload_png


# Generates a graph entirely in memory, uploads it to Vercel Blob, and returns its public URL.
# @param expr: The mathematical expression to plot.
# @param diff_var: The variable used as the graph's independent axis.
# @return: The complete public Vercel Blob URL of the generated PNG image.
async def graphic_generator(expr: str, diff_var: str) -> str:
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
