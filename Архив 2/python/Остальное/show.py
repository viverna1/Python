import numpy as np
import matplotlib.pyplot as plt


def function(*functions):
    x = np.arange(-10, 10.1, 0.1)
    for func in functions:
        if not isinstance(func, str):
            continue
        y = eval(func, {"np": np, "x": x})
        plt.plot(x, y, label=func)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.title("Графики функций")
    plt.show()


if __name__ == '__main__':
    function("2.5 * x**2 + 7.5 * x+5", "x")
