# MIT License © 2025 Anish Chaudhuri
# See full license at the bottom of this file.

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
