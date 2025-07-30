# MIT License © 2025 Anish Chaudhuri
# See full license at the bottom of this file.

import numpy as np
import math

class AdvancedMath:
    def __init__(self):
        pass

    # 🔢 MATRIX OPERATIONS
    def matrix_eigenvalues(self, A: np.ndarray) -> np.ndarray:
        """Returns the eigenvalues of a matrix."""
        return np.linalg.eigvals(A)

    def matrix_eigenvectors(self, A: np.ndarray) -> np.ndarray:
        """Returns the eigenvectors of a matrix."""
        return np.linalg.eig(A)[1]

    def lu_decomposition(self, A: np.ndarray):
        """Performs LU Decomposition (without SciPy)."""
        A = A.astype(float)
        n = len(A)
        L = np.eye(n)
        U = A.copy()
        for i in range(n):
            if U[i, i] == 0:
                raise ValueError("Matrix is singular!")
            for j in range(i + 1, n):
                factor = U[j, i] / U[i, i]
                L[j, i] = factor
                U[j] -= factor * U[i]
        return L, U

    def qr_decomposition(self, A: np.ndarray):
        """Performs QR Decomposition."""
        return np.linalg.qr(A)

    # 🔢 NUMBER THEORY
    def is_prime(self, n: int) -> bool:
        """Checks if a number is prime."""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def prime_factors(self, n: int) -> list:
        """Returns the prime factorization of a number."""
        factors = []
        i = 2
        while i * i <= n:
            while n % i == 0:
                factors.append(i)
                n //= i
            i += 1
        if n > 1:
            factors.append(n)
        return factors

    def mod_exp(self, base: int, exp: int, mod: int) -> int:
        """Computes (base^exp) % mod using fast modular exponentiation."""
        result = 1
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            base = (base * base) % mod
            exp //= 2
        return result

    # 🔢 COMBINATORICS
    def permutations(self, n: int, r: int) -> int:
        """Computes P(n, r) = n! / (n-r)!"""
        return math.factorial(n) // math.factorial(n - r)

    def combinations(self, n: int, r: int) -> int:
        """Computes C(n, r) = n! / (r! * (n-r)!)"""
        return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

    # 🔢 OPTIMIZATION
    def gradient_descent(self, f, df, x0: float, lr=0.01, tol=1e-6, max_iter=1000) -> float:
        """
        Gradient Descent Optimization.
        f  - function to minimize
        df - derivative of f
        x0 - initial guess
        lr - learning rate
        tol - stopping tolerance
        """
        x = x0
        for _ in range(max_iter):
            grad = df(x)
            if abs(grad) < tol:
                return x
            x -= lr * grad
        return x

    def linear_programming(self, A: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
        """
        Solves a basic linear programming problem: Minimize c^T * x
        Subject to: A * x ≤ b
        """
        from scipy.optimize import linprog
        res = linprog(c, A_ub=A, b_ub=b, method="highs")
        if res.success:
            return res.x
        return "No feasible solution"

    # 🔢 MATRIX UTILITIES
    def matrix_determinant(self, A: np.ndarray) -> float:
        """Returns the determinant of matrix A."""
        return np.linalg.det(A)

    def matrix_inverse(self, A: np.ndarray):
        """Returns the inverse of matrix A."""
        if np.linalg.det(A) == 0:
            return "Singular Matrix (No Inverse)"
        return np.linalg.inv(A)



import numpy as np

class AI:
    def __init__(self):
        pass

    # 🔥 MACHINE LEARNING MATH
    def mean_squared_error(self, y_true, y_pred):
        """Calculates Mean Squared Error (MSE)."""
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        return np.mean((y_true - y_pred) ** 2)

    def cross_entropy_loss(self, y_true, y_pred):
        """Calculates Cross Entropy Loss (for classification)."""
        y_true, y_pred = np.array(y_true), np.array(y_pred)  # Convert lists to NumPy arrays
        y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)  # Avoid log(0)
        return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

    # 🔥 ACTIVATION FUNCTIONS
    def sigmoid(self, x):
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-x))

    def relu(self, x):
        """ReLU activation function."""
        return np.maximum(0, x)

    def softmax(self, x):
        """Softmax activation function (for multi-class classification)."""
        exp_x = np.exp(x - np.max(x))  # For numerical stability
        return exp_x / np.sum(exp_x)

    # 🔥 NEURAL NETWORK BASICS
    def forward_propagation(self, X, W, b):
        """Computes forward pass in a simple neural network (XW + b)."""
        return np.dot(X, W) + b

    def backward_propagation(self, X, y, W, b, lr=0.01):
        """Performs basic backpropagation for a single-layer neural network."""
        m = X.shape[0]
        A = self.sigmoid(self.forward_propagation(X, W, b))
        dW = (1 / m) * np.dot(X.T, (A - y))
        db = (1 / m) * np.sum(A - y)
        W -= lr * dW
        b -= lr * db
        return W, b

    # 🔥 LINEAR REGRESSION
    def linear_regression(self, X, y):
        """Fits a simple linear regression model using least squares."""
        X = np.c_[np.ones(X.shape[0]), X]  # Add bias term
        return np.linalg.lstsq(X, y, rcond=None)[0]

    def polynomial_regression(self, X, y, degree=2):
        """Fits a polynomial regression model."""
        X_poly = np.vander(X, degree + 1)
        return np.linalg.lstsq(X_poly, y, rcond=None)[0]

    # 🔥 K-MEANS CLUSTERING (BASIC)
    def k_means(self, X, k, max_iters=100):
        """Performs K-Means clustering."""
        centroids = X[np.random.choice(X.shape[0], k, replace=False)]
        for _ in range(max_iters):
            labels = np.argmin(np.linalg.norm(X[:, None] - centroids, axis=2), axis=1)
            new_centroids = np.array([X[labels == j].mean(axis=0) for j in range(k)])
            if np.all(centroids == new_centroids):
                break
            centroids = new_centroids
        return centroids, labels


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



import math
import numpy as np

class BasicMath:
    def __init__(self):
        pass

    # 🔢 Basic Arithmetic Operations
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b): return a / b if b != 0 else "Undefined"
    def power(self, a, b): return a ** b
    def root(self, a, n): return a ** (1/n)
    def modulo(self, a, b): return a % b
    def factorial(self, n): return math.factorial(n)

    # 🔢 Algebra & Linear Algebra
    def gcd(self, a, b): return math.gcd(a, b)
    def lcm(self, a, b): return np.lcm(a, b)

    def matrix_inverse(self, A): return np.linalg.inv(A) if np.linalg.det(A) != 0 else "Singular Matrix"
    def matrix_determinant(self, A): return np.linalg.det(A)
    def matrix_eigenvalues(self, A): return np.linalg.eigvals(A)
    def matrix_eigenvectors(self, A): return np.linalg.eig(A)[1]

    def lu_decomposition(self, A):
        """LU Decomposition without SciPy"""
        A = A.astype(float)
        n = len(A)
        L = np.eye(n)
        U = A.copy()
        for i in range(n):
            for j in range(i + 1, n):
                factor = U[j, i] / U[i, i]
                L[j, i] = factor
                U[j] -= factor * U[i]
        return L, U

    def qr_decomposition(self, A):
        """QR Decomposition"""
        return np.linalg.qr(A)



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


import numpy as np
import math
import matplotlib.pyplot as plt
import itertools
import heapq

class OtherMath:
    def __init__(self):
        pass

    # 🔥 NUMBER THEORY - ADVANCED
    def lucas_number(self, n):
        """Returns the nth Lucas number."""
        if n == 0:
            return 2
        elif n == 1:
            return 1
        else:
            return self.lucas_number(n - 1) + self.lucas_number(n - 2)

    def collatz_sequence(self, n):
        """Generates the Collatz sequence for a given number."""
        sequence = [n]
        while n > 1:
            n = n // 2 if n % 2 == 0 else 3 * n + 1
            sequence.append(n)
        return sequence

    def partition_function(self, n):
        """Computes the partition function P(n) (number of ways n can be summed)."""
        partitions = [1] + [0] * n
        for k in range(1, n + 1):
            for j in range(k, n + 1):
                partitions[j] += partitions[j - k]
        return partitions[n]

    # 🔥 GRAPH THEORY
    def dijkstra(self, graph, start):
        """Finds the shortest path using Dijkstra's Algorithm."""
        queue = [(0, start)]
        distances = {node: float('inf') for node in graph}
        distances[start] = 0

        while queue:
            current_distance, current_node = heapq.heappop(queue)
            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))

        return distances

    def is_eulerian(self, graph):
        """Checks if a graph has an Eulerian path."""
        odd_degree_count = sum(1 for node in graph if len(graph[node]) % 2 != 0)
        return odd_degree_count in [0, 2]

    def euler_characteristic(self, V, E, F):
        """Computes Euler's characteristic χ = V - E + F for graphs and surfaces."""
        return V - E + F

    def random_graph(self, nodes, density=0.5):
        """Generates a random adjacency matrix for a graph."""
        matrix = np.random.rand(nodes, nodes) < density
        return np.triu(matrix, 1).astype(int) + np.triu(matrix, 1).T

    # 🔥 SPACIAL GEOMETRY
    def hypersphere_volume(self, r, d):
        """Computes the volume of a d-dimensional hypersphere."""
        return (np.pi ** (d / 2) / math.gamma(d / 2 + 1)) * (r ** d)

    def hypercube_volume(self, side, d):
        """Computes the volume of a d-dimensional hypercube."""
        return side ** d

    def distance_in_4d(self, p1, p2):
        """Computes Euclidean distance in 4D space."""
        return np.linalg.norm(np.array(p1) - np.array(p2))

    # 🔥 RANDOMIZED MATH
    def monte_carlo_pi(self, samples=10000):
        """Estimates π using Monte Carlo method."""
        inside = sum(np.sum(np.random.rand(samples, 2) ** 2, axis=1) <= 1)
        return (inside / samples) * 4

    def random_walk(self, steps=10):
        """Generates a simple 1D random walk."""
        walk = [0]
        for _ in range(steps):
            walk.append(walk[-1] + np.random.choice([-1, 1]))
        return walk

    # 🔥 PROCEDURAL GENERATION
    def perlin_noise(self, size, scale=10, show_graph=True):
        """Generates a 1D Perlin noise array and optionally plots it."""
        x = np.linspace(0, scale, size)
        noise = np.sin(2 * np.pi * x) + np.random.normal(scale=0.2, size=size)

        if show_graph:
            plt.plot(x, noise, label="Perlin Noise")
            plt.xlabel("X")
            plt.ylabel("Noise Value")
            plt.title("Perlin Noise Generation")
            plt.legend()
            plt.grid()
            plt.show()

        return noise

    def fractal_dimension(self, Z, threshold=0.5, show_graph=True):
        """Computes the fractal dimension of a 2D array using box-counting."""
        def boxcount(Z, k):
            S = np.add.reduceat(
                np.add.reduceat(Z, np.arange(0, Z.shape[0], k), axis=0),
                np.arange(0, Z.shape[1], k), axis=1
            )
            return np.count_nonzero(S)

        Z = (Z > threshold)  # Convert to binary
        sizes = 2 ** np.arange(int(np.log2(Z.shape[0])), 0, -1)
        counts = np.array([boxcount(Z, size) for size in sizes])

        valid_indices = counts > 0
        if np.any(valid_indices):
            coeffs = np.polyfit(np.log(sizes[valid_indices]), np.log(counts[valid_indices]), 1)
            fractal_dim = -coeffs[0]
        else:
            fractal_dim = "Undefined (Invalid Fractal Data)"

        if show_graph:
            plt.imshow(Z, cmap="binary")
            plt.title(f"Fractal Structure (Dimension: {fractal_dim})")
            plt.colorbar()
            plt.show()

        return fractal_dim



import numpy as np
import math

class ScientificMath:
    def __init__(self):
        pass

    # 🔥 THERMODYNAMICS
    def heat_transfer(self, mass, specific_heat, temp_change):
        """Calculates heat transfer using Q = mcΔT."""
        return mass * specific_heat * temp_change

    def entropy_change(self, heat, temp):
        """Calculates entropy change using ΔS = Q / T."""
        return heat / temp if temp != 0 else "Undefined"

    def ideal_gas_law(self, pressure, volume, moles, R=8.314):
        """Calculates temperature using PV = nRT."""
        return (pressure * volume) / (moles * R)

    # ⚛️ QUANTUM MECHANICS
    def wave_energy(self, frequency):
        """Calculates energy of a wave using E = h * f."""
        h = 6.626e-34  # Planck’s constant
        return h * frequency

    def schrodinger_energy(self, n, mass, length):
        """Calculates energy levels in a quantum box using E_n = (n^2 * h^2) / (8mL^2)."""
        h = 6.626e-34  # Planck’s constant
        return (n**2 * h**2) / (8 * mass * length**2)

    # 🧪 CHEMISTRY
    def molecular_weight(self, elements, amounts):
        """Calculates molecular weight given elements and their amounts."""
        atomic_weights = {
            "H": 1.008, "C": 12.011, "O": 15.999, "N": 14.007, "Na": 22.990,
            "Cl": 35.45, "Fe": 55.845, "S": 32.065, "P": 30.974
        }
        return sum(atomic_weights[e] * a for e, a in zip(elements, amounts) if e in atomic_weights)

    def reaction_rate(self, k, concentrations, orders):
        """Calculates reaction rate using rate = k * [A]^m * [B]^n ..."""
        return k * np.prod([conc**order for conc, order in zip(concentrations, orders)])

    # 🌌 ASTRONOMY
    def orbital_velocity(self, mass, radius):
        """Calculates orbital velocity using v = sqrt(GM/R)."""
        G = 6.67430e-11  # Gravitational constant
        return np.sqrt(G * mass / radius)

    def escape_velocity(self, mass, radius):
        """Calculates escape velocity using v = sqrt(2GM/R)."""
        G = 6.67430e-11  # Gravitational constant
        return np.sqrt(2 * G * mass / radius)

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
