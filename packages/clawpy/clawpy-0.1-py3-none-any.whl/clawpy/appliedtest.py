#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "./")
from applied_math import AppliedMath

# Create an instance of AppliedMath
applied_math = AppliedMath()

print("\n **Applied Math Tests**")

# **Physics**
print("Aerodynamic Lift (rho=1.225, v=30 m/s, A=2 m^2, C_L=0.5):", applied_math.aerodynamic_lift(1.225, 30, 2, 0.5))

# **AI Math Generator**
if hasattr(applied_math, "generate_math_problem"):
    problem, answer = applied_math.generate_math_problem("medium")
    print(f"Generated Problem: {problem}\nAnswer: {answer}")
else:
    print("generate_math_problem() is missing in AppliedMath.")

# **Math Visualization**
if hasattr(applied_math, "generate_plot"):
    x, y = applied_math.generate_plot(lambda x: x**2)
    print("Generated Plot Data (First 5 Points):")
    for i in range(5):
        print(f"x: {x[i]}, y: {y[i]}")
else:
    print("generate_plot() is missing in AppliedMath.")
