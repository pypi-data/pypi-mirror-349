import sys
import os

# Import the module
import basic_math as basic_math

# Create an instance of the class
math_obj = basic_math.BasicMath()

# Run tests
print(" **Basic Math Tests**")
print("Addition (5 + 3):", math_obj.add(5, 3))  
print("Subtraction (10 - 4):", math_obj.subtract(10, 4))  
print("Multiplication (6 * 7):", math_obj.multiply(6, 7))  
print("Division (10 / 2):", math_obj.divide(10, 2))  
print("Power (2^3):", math_obj.power(2, 3))  
print("Root (27^(1/3)): ", math_obj.root(27, 3))  
print("Modulo (10 mod 3):", math_obj.modulo(10, 3))  
print("Factorial of 5:", math_obj.factorial(5))  
