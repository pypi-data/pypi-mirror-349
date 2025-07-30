import numpy as np
import sympy as sp
import random

class MoreMath:

    @staticmethod
    def distance_in_nD(p1, p2):
        """Calculates Euclidean distance in n-dimensional space."""
        p1 = np.array(p1)
        p2 = np.array(p2)
        return np.linalg.norm(p1 - p2)

    @staticmethod
    def generate_random_graph(num_nodes, edge_prob=0.3):
        """Generates a random undirected graph using an adjacency matrix."""
        graph = np.zeros((num_nodes, num_nodes), dtype=int)
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if random.random() < edge_prob:
                    graph[i][j] = graph[j][i] = 1
        return graph

    @staticmethod
    def fourier_transform(signal):
        """Computes the discrete Fourier Transform of a 1D signal."""
        return np.fft.fft(signal)

    @staticmethod
    def solve_equation(equation, var):
        """Solves a symbolic equation (use sympy symbols)."""
        return sp.solve(equation, var)

    @staticmethod
    def qr_decomposition(matrix):
        """Performs QR Decomposition of a matrix."""
        return np.linalg.qr(matrix)

    @staticmethod
    def matrix_eigenvalues(matrix):
        """Returns eigenvalues of a matrix."""
        return np.linalg.eigvals(matrix)

    @staticmethod
    def matrix_eigenvectors(matrix):
        """Returns eigenvectors of a matrix."""
        _, vecs = np.linalg.eig(matrix)
        return vecs

    @staticmethod
    def matrix_inverse(matrix):
        """Returns the inverse of a matrix."""
        return np.linalg.inv(matrix)
