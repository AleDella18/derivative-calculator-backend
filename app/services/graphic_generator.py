from pathlib import Path
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, lambdify


# Generates the graphic of the given expression and saves it as a PNG file.
# @param expr: the expression to plot.
# @param diff_var:  The variable with respect to which the differentiation is performed.
# @param image_name: The name of the generated PNG file (without extension).
# @return: The relative path of the generated PNG file.
def graphic_generator(expr, diff_var, image_name):
    x_vals = np.linspace(-50, 50, 100)

    x = symbols(diff_var)
    f = lambdify(x, sympify(expr), "numpy")
    y_vals = f(x_vals)

    if np.isscalar(y_vals):
        y_vals = np.full_like(x_vals, y_vals)

    plt.figure()
    plt.plot(x_vals, y_vals, label=expr)
    plt.legend()

    project_root = Path(__file__).resolve().parents[2]
    imgs_folder = project_root / "imgs"
    imgs_folder.mkdir(exist_ok=True)

    filename = f"{image_name}.png"

    absolute_path = imgs_folder / filename
    relative_path = Path("imgs") / filename

    plt.savefig(absolute_path, dpi=300, bbox_inches="tight")
    plt.close()

    return str(relative_path)