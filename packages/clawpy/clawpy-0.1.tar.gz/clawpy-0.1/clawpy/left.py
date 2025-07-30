# MIT License © 2025 Anish Chaudhuri
# See full license at the bottom of this file.

import numpy as np
import math
import matplotlib.pyplot as plt
from itertools import product
from matplotlib.animation import FuncAnimation

class LeftMath:
    def __init__(self):
        pass

    # 🔹 **Complex & Imaginary Numbers**
    def complex_magnitude(self, z):
        return abs(complex(z))

    def complex_phase(self, z):
        return np.angle(complex(z))

    def complex_conjugate(self, z):
        return np.conj(complex(z))

    def imaginary_root(self, n):
        return np.sqrt(complex(n))

    # 🔹 **Hyperbolic Trigonometry**
    def sinh(self, x):
        return np.sinh(x)

    def cosh(self, x):
        return np.cosh(x)

    def tanh(self, x):
        return np.tanh(x)

    # 🔹 **Fibonacci, Golden Ratio & Pascal's Triangle**
    def fibonacci(self, n):
        fib = [0, 1]
        for i in range(2, n + 1):
            fib.append(fib[-1] + fib[-2])
        return fib[n]

    def golden_ratio(self):
        return (1 + 5 ** 0.5) / 2

    def pascal_triangle(self, n):
        triangle = [[1]]
        for i in range(1, n):
            row = [1]
            for j in range(len(triangle[-1]) - 1):
                row.append(triangle[-1][j] + triangle[-1][j + 1])
            row.append(1)
            triangle.append(row)
        return triangle

    # 🔹 **Prime Number Theory**
    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def prime_factors(self, n):
        factors = []
        i = 2
        while i * i <= n:
            if n % i:
                i += 1
            else:
                n //= i
                factors.append(i)
        if n > 1:
            factors.append(n)
        return factors

    def next_prime(self, n):
        num = n + 1
        while not self.is_prime(num):
            num += 1
        return num

    # 🔹 **Mensuration (Geometry)**
    def circle_area(self, r):
        return math.pi * r ** 2

    def sphere_volume(self, r):
        return (4 / 3) * math.pi * r ** 3

    def cylinder_volume(self, r, h):
        return math.pi * r ** 2 * h

    def cone_volume(self, r, h):
        return (1 / 3) * math.pi * r ** 2 * h

    def pyramid_volume(self, base_area, h):
        return (1 / 3) * base_area * h

    # 🔹 **4D Tesseract (Hypercube) Animation**
    def draw_tesseract(self):
        """Visualizes a rotating 4D Hypercube Projection."""
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Generate 4D hypercube (16 vertices)
        edges = []
        vertices = np.array(list(product([-1, 1], repeat=4)))  # 16 vertices in 4D
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                if np.sum(np.abs(vertices[i] - vertices[j])) == 2:  # Edge check
                    edges.append((i, j))

        # Project 4D to 3D
        def project_4d_to_3d(vertices, angle=0):
            rotation_matrix = np.array([
                [np.cos(angle), -np.sin(angle), 0, 0],
                [np.sin(angle), np.cos(angle), 0, 0],
                [0, 0, np.cos(angle), -np.sin(angle)],
                [0, 0, np.sin(angle), np.cos(angle)]
            ])
            return vertices @ rotation_matrix.T[:, :3]  # Taking first 3 columns for projection

        lines = [ax.plot([], [], [], 'r')[0] for _ in edges]  # Edge placeholders

        def update(frame):
            ax.clear()
            ax.set_xlim([-2, 2])
            ax.set_ylim([-2, 2])
            ax.set_zlim([-2, 2])
            ax.set_title(f"4D Hypercube (Frame {frame})")

            # Get rotated projected points
            projected_vertices = project_4d_to_3d(vertices, angle=frame * 0.05)

            for i, (start, end) in enumerate(edges):
                x, y, z = zip(*[projected_vertices[start], projected_vertices[end]])
                lines[i].set_data(x, y)
                lines[i].set_3d_properties(z)
                ax.add_line(lines[i])

            return lines

        ani = FuncAnimation(fig, update, frames=200, interval=20, blit=False)
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
