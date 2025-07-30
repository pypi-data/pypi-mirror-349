# MIT License © 2025 Anish Chaudhuri
# See full license at the bottom of this file.

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
