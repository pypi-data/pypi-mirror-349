import sys
sys.path.insert(0, "./")  # ✅ Adds main directory to search path

from other import OtherMath  # ✅ NOW IT WORKS!

import numpy as np

other_math = OtherMath()

print("\n **OtherMath Tests**\n")

# 🟢 NUMBER THEORY
print(" **Number Theory**")
print("Lucas Number (n=10):", other_math.lucas_number(10))
print("Collatz Sequence (n=13):", other_math.collatz_sequence(13))
print("Partition Function P(5):", other_math.partition_function(5))

# 🟢 GRAPH THEORY
print("\n **Graph Theory**")
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}
print("Dijkstra's Shortest Path from A:", other_math.dijkstra(graph, 'A'))
print("Graph is Eulerian?:", other_math.is_eulerian(graph))
print("Euler Characteristic (V=5, E=7, F=3):", other_math.euler_characteristic(5, 7, 3))
print("Random Graph (5 Nodes):\n", other_math.random_graph(5))  # ✅ FIXED

# 🟢 SPACIAL GEOMETRY
print("\n **Spacial Geometry**")
print("Hypersphere Volume (r=3, d=4):", other_math.hypersphere_volume(3, 4))
print("Hypercube Volume (side=3, d=4):", other_math.hypercube_volume(3, 4))
print("Distance in 4D ([1,2,3,4] to [4,5,6,7]):", other_math.distance_in_4d([1,2,3,4], [4,5,6,7]))

# 🟢 RANDOMIZED MATH
print("\n **Randomized Math**")
print("Monte Carlo Pi Approximation (100000 samples):", other_math.monte_carlo_pi(100000))
print("Random Walk (10 Steps):", other_math.random_walk(10))

# 🟢 PROCEDURAL GENERATION
print("\n **Procedural Generation**")
print("Perlin Noise (10 Points):", other_math.perlin_noise(10, show_graph=True))  # ✅ Graph appears
print("Fractal Dimension (Random 10x10 Matrix):", other_math.fractal_dimension(np.random.rand(10,10), show_graph=True))  # ✅ Graph appears
