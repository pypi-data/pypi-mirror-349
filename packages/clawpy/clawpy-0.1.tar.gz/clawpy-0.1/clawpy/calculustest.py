import sys
sys.path.insert(0, "./")  
from calculus import Calculus  # Import the Calculus class
import numpy as np

# Create an instance of Calculus
calc = Calculus()

print("\n **Calculus Tests**")

# 📈 DIFFERENTIATION TESTS
def f(x): return x**3 + 2*x**2 + x  # Sample function: f(x) = x³ + 2x² + x

x_val = 2
print("\n **Differentiation**")
print(f"Derivative of f(x) at x={x_val}:", calc.derivative(f, x_val))
print(f"Second Derivative of f(x) at x={x_val}:", calc.second_derivative(f, x_val))

def f_partial(x, y): return x**2 + y**2  # Sample function for partial derivatives

print(f"Partial Derivative w.r.t x at (2,3):", calc.partial_derivative(f_partial, 2, 3, var="x"))
print(f"Partial Derivative w.r.t y at (2,3):", calc.partial_derivative(f_partial, 2, 3, var="y"))

# 📉 INTEGRATION TESTS
print("\n **Integration**")
print("Integral of f(x) from 0 to 2:", calc.integrate(f, 0, 2))

def f_double(x, y): return x * y  # Sample function for double integral

print("Double Integral of f(x,y) over [0,2]x[0,2]:", calc.double_integral(f_double, (0, 2), (0, 2)))

# 🔀 DIFFERENTIAL EQUATIONS TESTS
def df(x, y): return x + y  # dy/dx = x + y

print("\n **Differential Equations**")
print("Euler Method (dy/dx = x+y, x0=0, y0=1, h=0.1, steps=10):", 
      calc.euler_method(df, x0=0, y0=1, h=0.1, steps=10))

print("Runge-Kutta Method (dy/dx = x+y, x0=0, y0=1, h=0.1, steps=10):", 
      calc.runge_kutta(df, x0=0, y0=1, h=0.1, steps=10))

# 🎵 FOURIER & LAPLACE TRANSFORMS TESTS
def f_t(t): return np.sin(2 * np.pi * t)  # Sample function for Fourier Transform

print("\n **Fourier & Laplace Transforms**")
print("Fourier Transform (sin wave, t=[0,10]):", calc.fourier_transform(f_t, (0, 10))[:5])  # Show first 5 values

print("Laplace Transform (e^(-t), s=1):", calc.laplace_transform(lambda t: np.exp(-t), s=1))
