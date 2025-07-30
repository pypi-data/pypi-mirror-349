# MIT License © 2025 Anish Chaudhuri
# See full license at the bottom of this file.

import numpy as np

class Calculus:
    def __init__(self):
        pass

    # 📈 DIFFERENTIATION
    def derivative(self, f, x, h=1e-5):
        """Computes the derivative of f at x using central difference method."""
        return (f(x + h) - f(x - h)) / (2 * h)

    def second_derivative(self, f, x, h=1e-5):
        """Computes the second derivative of f at x."""
        return (f(x + h) - 2 * f(x) + f(x - h)) / (h**2)

    def partial_derivative(self, f, x, y, var="x", h=1e-5):
        """Computes the partial derivative of f(x,y) with respect to x or y."""
        if var == "x":
            return (f(x + h, y) - f(x - h, y)) / (2 * h)
        elif var == "y":
            return (f(x, y + h) - f(x, y - h)) / (2 * h)
        else:
            return "Invalid variable"

    # 📉 INTEGRATION
    def integrate(self, f, a, b, n=1000):
        """Computes the definite integral of f from a to b using the Trapezoidal Rule."""
        x = np.linspace(a, b, n)
        y = f(x)
        return np.trapz(y, x)

    def double_integral(self, f, x_range, y_range, n=100):
        """Computes a double integral over a given range using a 2D Trapezoidal Rule."""
        x = np.linspace(x_range[0], x_range[1], n)
        y = np.linspace(y_range[0], y_range[1], n)
        X, Y = np.meshgrid(x, y)
        Z = np.vectorize(f)(X, Y)
        return np.trapz(np.trapz(Z, x, axis=0), y, axis=0)

    # 🔀 DIFFERENTIAL EQUATIONS
    def euler_method(self, df, x0, y0, h, steps):
        """Solves dy/dx = df(x, y) using Euler's method."""
        x, y = x0, y0
        result = [y]
        for _ in range(steps):
            y += h * df(x, y)
            x += h
            result.append(y)
        return np.array(result)

    def runge_kutta(self, df, x0, y0, h, steps):
        """Solves dy/dx = df(x, y) using 4th-order Runge-Kutta method."""
        x, y = x0, y0
        result = [y]
        for _ in range(steps):
            k1 = h * df(x, y)
            k2 = h * df(x + h / 2, y + k1 / 2)
            k3 = h * df(x + h / 2, y + k2 / 2)
            k4 = h * df(x + h, y + k3)
            y += (k1 + 2 * k2 + 2 * k3 + k4) / 6
            x += h
            result.append(y)
        return np.array(result)

    # 🎵 FOURIER & LAPLACE TRANSFORMS
    def fourier_transform(self, f, t_range, n=1000):
        """Computes the Fourier Transform of a function over a given range."""
        t = np.linspace(t_range[0], t_range[1], n)
        y = f(t)
        return np.fft.fft(y)

    def laplace_transform(self, f, s, t_max=10, n=1000):
        """Computes the Laplace Transform using numerical integration."""
        t = np.linspace(0, t_max, n)
        y = np.vectorize(f)(t) * np.exp(-s * t)
        return np.trapz(y, t)

# MIT License
#
# Copyright (c) 2025 Anish Chaudhuri
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
