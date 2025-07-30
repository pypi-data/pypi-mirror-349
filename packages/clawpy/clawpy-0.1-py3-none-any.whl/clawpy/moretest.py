from more import MoreMath as mm
import numpy as np
import sympy as sp
import time

start_time = time.time()

print("\n=== Extended Math Test Suite (more.py) ===\n")

print("** Distance in N-Dimensional Space **")
p1 = [1, 2, 3]
p2 = [4, 5, 6]
print("Points:", p1, p2)
print("Distance:", mm.distance_in_nD(p1, p2), "\n")

print("** Random Graph Generation **")
graph = mm.generate_random_graph(5, edge_prob=0.4)
print("Adjacency Matrix:\n", graph, "\n")

print("** Fourier Transform **")
signal = [0, 1, 0, -1]
fft = mm.fourier_transform(signal)
print("Signal:", signal)
print("Fourier Transform:", fft, "\n")

print("** Equation Solving **")
x = sp.symbols('x')
equation = x**2 - 4
solutions = mm.solve_equation(equation, x)
print("Equation:", equation)
print("Solutions:", solutions, "\n")

print("** QR Decomposition **")
A = np.array([[1, 2], [3, 4]])
Q, R = mm.qr_decomposition(A)
print("Matrix A:\n", A)
print("Q:\n", Q)
print("R:\n", R, "\n")

print("** Eigenvalues and Eigenvectors **")
eigenvals = mm.matrix_eigenvalues(A)
eigenvecs = mm.matrix_eigenvectors(A)
print("Eigenvalues:", eigenvals)
print("Eigenvectors:\n", eigenvecs, "\n")

print("** Matrix Inversion **")
inv = mm.matrix_inverse(A)
print("Inverse of A:\n", inv)

print("\n=== All Tests Completed Successfully ===")

end_time = time.time()
total_time = end_time - start_time

print(f"\n **All More Tests Completed in {total_time:.4f} seconds!** \n")
