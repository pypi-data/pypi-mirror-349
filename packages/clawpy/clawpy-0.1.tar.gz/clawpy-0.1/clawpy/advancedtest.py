import numpy as np
from advanced_math import AdvancedMath
import time
import math


start_time = time.time()

def main():
    adv_math = AdvancedMath()

    print("\n=== Advanced Math Full Test Suite ===\n")

    # --- MATRIX OPERATIONS ---
    print("** Matrix Operations **")
    A = np.array([[4, 2], [3, 1]])
    print("Matrix A:\n", A)

    ops = adv_math.matrix_operations(A)
    print("Eigenvalues:", ops['eigenvalues'])
    print("Eigenvectors:\n", ops['eigenvectors'])

    L, U = ops['LU']
    print("LU Decomposition:")
    print("L:\n", L)
    print("U:\n", U)

    Q, R = ops['QR']
    print("QR Decomposition:")
    print("Q:\n", Q)
    print("R:\n", R)

    print("Determinant:", ops['determinant'])
    print("Inverse:\n", ops['inverse'])

    # --- NUMBER THEORY ---
    print("\n** Number Theory **")
    n_prime = 37
    print(f"Is {n_prime} prime? {adv_math.is_prime(n_prime)}")

    n_factors = 56
    print(f"Prime factors of {n_factors}: {adv_math.prime_factors(n_factors)}")

    base, exp, mod = 3, 13, 7
    print(f"Modular exponentiation: ({base}^{exp} % {mod}) = {adv_math.mod_exp(base, exp, mod)}")

    # --- COMBINATORICS ---
    print("\n** Combinatorics **")
    n_perm, r_perm = 5, 3
    print(f"Permutations P({n_perm}, {r_perm}): {adv_math.permutations(n_perm, r_perm)}")

    n_comb, r_comb = 5, 3
    print(f"Combinations C({n_comb}, {r_comb}): {adv_math.combinations(n_comb, r_comb)}")

    # --- OPTIMIZATION ---
    print("\n** Optimization **")

    # Test function: f(x) = (x-3)^2 with derivative 2*(x-3)
    f = lambda x: (x - 3) ** 2
    df = lambda x: 2 * (x - 3)
    x0 = 0

   

if __name__ == "__main__":
    main()

end_time = time.time()
total_time = end_time - start_time

print(f"\n **All ClawPy Tests Completed in {total_time:.4f} seconds!** \n")