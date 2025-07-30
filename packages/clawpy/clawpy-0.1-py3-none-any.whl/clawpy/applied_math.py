# MIT License © 2025 Anish Chaudhuri
# See full license at the bottom of this file.

import numpy as np
import matplotlib.pyplot as plt
import random

class AppliedMath:
    def __init__(self):
        pass

    # ⚡ PHYSICS FUNCTIONS
    def newton_second_law(self, force, mass):
        """Calculates acceleration using F = ma."""
        return force / mass if mass != 0 else "Undefined"

    def kinetic_energy(self, mass, velocity):
        """Calculates kinetic energy: KE = 0.5 * m * v^2."""
        return 0.5 * mass * velocity**2

    def ohms_law(self, voltage, resistance):
        """Calculates current using Ohm's Law: V = IR."""
        return voltage / resistance if resistance != 0 else "Undefined"

    def gravitational_force(self, m1, m2, r):
        """Calculates gravitational force using Newton's Law of Gravitation."""
        G = 6.67430e-11  # Gravitational constant
        return G * (m1 * m2) / (r**2) if r != 0 else "Undefined"

    def aerodynamic_lift(self, rho, v, A, C_L):
        """Calculates aerodynamic lift: L = 0.5 * rho * v^2 * A * C_L."""
        return 0.5 * rho * v**2 * A * C_L

    # 📊 STATISTICS FUNCTIONS
    def mean(self, data):
        """Calculates the mean of a dataset."""
        return np.mean(data)

    def variance(self, data):
        """Calculates variance of a dataset."""
        return np.var(data)

    def standard_deviation(self, data):
        """Calculates standard deviation."""
        return np.std(data)

    def correlation_coefficient(self, x, y):
        """Computes Pearson correlation coefficient."""
        return np.corrcoef(x, y)[0, 1]

    # 🎯 AI MATH GENERATOR
    def generate_math_problem(self, difficulty="medium"):
        """Generates a random math problem based on difficulty."""
        if difficulty == "easy":
            a, b = random.randint(1, 10), random.randint(1, 10)
            problem = f"{a} + {b} = ?"
            answer = a + b
        elif difficulty == "medium":
            a, b = random.randint(1, 20), random.randint(1, 20)
            problem = f"{a} × {b} = ?"
            answer = a * b
        elif difficulty == "hard":
            a = random.randint(2, 10)
            problem = f"{a}² = ?"
            answer = a ** 2
        else:
            return "Invalid difficulty", None
        return problem, answer

    # 🎵 SIGNAL PROCESSING
    def fourier_transform(self, signal):
        """Computes Discrete Fourier Transform (DFT)."""
        return np.fft.fft(signal)

    def inverse_fourier_transform(self, signal):
        """Computes Inverse Fourier Transform."""
        return np.fft.ifft(signal)

    def convolution(self, signal1, signal2):
        """Computes convolution of two signals."""
        return np.convolve(signal1, signal2, mode='full')

    # 📈 GRAPHING FUNCTIONS
    def generate_plot(self, func, start=-10, end=10, num_points=100):
        """Generates x, y points for plotting a function."""
        x = np.linspace(start, end, num_points)
        y = np.vectorize(func)(x)
        return x, y

    def plot_function(self, func, start=-10, end=10, num_points=100):
        """Plots a mathematical function."""
        x, y = self.generate_plot(func, start, end, num_points)
        plt.plot(x, y)
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title("Function Plot")
        plt.grid()
        plt.show()

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
