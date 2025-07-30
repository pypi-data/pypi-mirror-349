# MIT License © 2025 Anish Chaudhuri
# See full license at the bottom of this file.

import numpy as np
import math

class AdvancedMath:

    def matrix_operations(self, matrix):
        """Performs various matrix operations"""
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        L, U = self.lu_decomposition(matrix)
        Q, R = np.linalg.qr(matrix)
        determinant = np.linalg.det(matrix)
        inverse = np.linalg.inv(matrix)
        return {
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'LU': (L, U),
            'QR': (Q, R),
            'determinant': determinant,
            'inverse': inverse
        }

    def lu_decomposition(self, matrix):
        """Performs LU decomposition using Doolittle's method"""
        n = len(matrix)
        L = np.zeros((n, n))
        U = np.zeros((n, n))
        matrix = np.array(matrix)

        for i in range(n):
            L[i][i] = 1
            for j in range(i, n):
                sum = 0
                for k in range(i):
                    sum += L[i][k] * U[k][j]
                U[i][j] = matrix[i][j] - sum

            for j in range(i + 1, n):
                sum = 0
                for k in range(i):
                    sum += L[j][k] * U[k][i]
                L[j][i] = (matrix[j][i] - sum) / U[i][i]

        return L, U

    def is_prime(self, num):
        """Check if a number is prime"""
        if num <= 1:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    def prime_factors(self, num):
        """Returns the prime factors of a number"""
        i = 2
        factors = []
        while i * i <= num:
            if num % i:
                i += 1
            else:
                num //= i
                factors.append(i)
        if num > 1:
            factors.append(num)
        return factors

    def mod_exp(self, base, exp, mod):
        """Performs modular exponentiation: (base^exp) % mod"""
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp // 2
            base = (base * base) % mod
        return result

    def permutations(self, n: int, r: int) -> int:
        """Computes P(n, r) = n! / (n-r)!"""
        return math.factorial(n) // math.factorial(n - r)

    def combinations(self, n: int, r: int) -> int:
        """Computes C(n, r) = n! / (r! * (n-r)!)"""
        return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))




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
