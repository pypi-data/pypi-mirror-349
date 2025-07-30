import clawpy
import numpy as np

# Create an instance of AdvancedMath
adv_math = AdvancedMath()

print("\n🔹 **Advanced Math Tests**")

# 🔢 MATRIX OPERATIONS TESTS
A = np.array([[4, 2], [3, 1]])

print("\n🟢 **Matrix Operations**")
print("Matrix Eigenvalues:", adv_math.matrix_eigenvalues(A))
print("Matrix Eigenvectors:\n", adv_math.matrix_eigenvectors(A))

L, U = adv_math.lu_decomposition(A)
print("\nLU Decomposition:\nL:\n", L, "\nU:\n", U)

Q, R = adv_math.qr_decomposition(A)
print("\nQR Decomposition:\nQ:\n", Q, "\nR:\n", R)

print("\nMatrix Determinant:", adv_math.matrix_determinant(A))
print("Matrix Inverse:\n", adv_math.matrix_inverse(A))

# 🔢 NUMBER THEORY TESTS
print("\n🟢 **Number Theory**")
num = 37
print(f"Is {num} Prime?:", adv_math.is_prime(num))
print("Prime Factors of 56:", adv_math.prime_factors(56))
print("Modular Exponentiation (3^13 % 7):", adv_math.mod_exp(3, 13, 7))

# 🔢 COMBINATORICS TESTS
print("\n🟢 **Combinatorics**")
print("Permutations P(5, 3):", adv_math.permutations(5, 3))
print("Combinations C(5, 3):", adv_math.combinations(5, 3))

# 🔢 OPTIMIZATION TESTS
print("\n🟢 **Optimization**")

# Gradient Descent Test (Minimizing f(x) = x^2)
def f(x): return x**2
def df(x): return 2*x

print("Gradient Descent (Minimizing x^2, Start at x=5):", adv_math.gradient_descent(f, df, 5))

# Linear Programming Test
A_lp = np.array([[2, 1], [1, 1]])
b_lp = np.array([4, 3])
c_lp = np.array([3, 2])

print("Linear Programming Solution:", adv_math.linear_programming(A_lp, b_lp, c_lp))
