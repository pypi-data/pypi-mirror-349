import sys
import os

# ✅ Import LeftMath
from left import LeftMath  

# ✅ Initialize LeftMath
lm = LeftMath()

print("\n **LeftMath Tests**\n")

# ✅ **Complex & Imaginary Numbers**
print(" **Complex & Imaginary Numbers**")
print(f"Complex Magnitude: {lm.complex_magnitude(3 + 4j)}")
print(f"Complex Phase (radians): {lm.complex_phase(3 + 4j)}")
print(f"Complex Conjugate: {lm.complex_conjugate(3 + 4j)}")
print(f"Imaginary Root of -4: {lm.imaginary_root(-4)}\n")

# ✅ **Hyperbolic Trigonometry**
print(" **Hyperbolic Trigonometry**")
print(f"sinh(2): {lm.sinh(2)}")
print(f"cosh(2): {lm.cosh(2)}")
print(f"tanh(2): {lm.tanh(2)}\n")

# ✅ **Fibonacci, Golden Ratio & Pascal's Triangle**
print(" **Fibonacci, Golden Ratio & Pascal's Triangle**")
print(f"Golden Ratio: {lm.golden_ratio()}")
print(f"Fibonacci(10): {lm.fibonacci(10)}")
print(f"Pascal's Triangle (5 rows): {lm.pascal_triangle(5)}\n")

# ✅ **Prime Number Theory**
print(" **Prime Number Theory**")
print(f"Is 97 Prime?: {lm.is_prime(97)}")
print(f"Prime Factors of 56: {lm.prime_factors(56)}")
print(f"Next Prime after 100: {lm.next_prime(100)}\n")

# ✅ **Mensuration (Geometry)**
print(" **Mensuration (Geometry)**")
print(f"Circle Area (r=5): {lm.circle_area(5)}")
print(f"Sphere Volume (r=3): {lm.sphere_volume(3)}")
print(f"Cylinder Volume (r=3, h=5): {lm.cylinder_volume(3, 5)}")
print(f"Cone Volume (r=3, h=5): {lm.cone_volume(3, 5)}")
print(f"Pyramid Volume (Base=10, h=6): {lm.pyramid_volume(10, 6)}\n")

# ✅ **4D Tessellation (Tesseract)**
print(" Running 4D Tesseract Animation... (Close the window to continue)")
lm.draw_tesseract()

print(" **LeftMath Tests Completed!** \n")
