# MIT License © 2025 Anish Chaudhuri
# See full license at the bottom of this file.

import sys
import os

# 🔥 Fix Import Errors by Adding `clawpy/` to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ✅ Import all modules
from .basic_math import BasicMath
from .calculus import Calculus
from .advanced_math import AdvancedMath
from .applied_math import AppliedMath
from .ai import AI
from .scientific import ScientificMath
from .left import LeftMath
from .other import OtherMath  # 🚀 Now includes `random.py` functionality!
from .more import MoreMath

# ✅ Create instances of each module
_basic_math = BasicMath()
_calculus_math = Calculus()
_advanced_math = AdvancedMath()
_applied_math = AppliedMath()
_ai_math = AI()
_scientific_math = ScientificMath()
_left_math = LeftMath()
_other_math = OtherMath()  # 🔥 Now includes Spacial Geometry, Chaos Math, Graphs, etc.
_more_math = MoreMath()

# ✅ Expose functions at the package level

# 🔢 **Basic Math**
add = _basic_math.add
subtract = _basic_math.subtract
multiply = _basic_math.multiply
divide = _basic_math.divide
power = _basic_math.power
root = _basic_math.root
modulo = _basic_math.modulo
factorial = _basic_math.factorial

# 🔢 **Algebra & Linear Algebra**
gcd = _basic_math.gcd
lcm = _basic_math.lcm
lu_decomposition = _advanced_math.lu_decomposition

# 🔢 **Calculus**
derivative = _calculus_math.derivative
integrate = _calculus_math.integrate

# 🔢 **AI & Machine Learning**
mean_squared_error = _ai_math.mean_squared_error
cross_entropy_loss = _ai_math.cross_entropy_loss
sigmoid = _ai_math.sigmoid
relu = _ai_math.relu
softmax = _ai_math.softmax

# 🔢 **Scientific & Applied Math**
newton_second_law = _applied_math.newton_second_law
kinetic_energy = _applied_math.kinetic_energy

# 🔢 **Prime Number Theory & Fibonacci (From LeftMath)**
is_prime = _left_math.is_prime
fibonacci = _left_math.fibonacci
golden_ratio = _left_math.golden_ratio
prime_factors = _left_math.prime_factors
next_prime = _left_math.next_prime

# 🔢 **Graph Theory (From OtherMath)**
dijkstra = _other_math.dijkstra
is_eulerian = _other_math.is_eulerian
euler_characteristic = _other_math.euler_characteristic

# 🔢 **Spacial Geometry (From OtherMath)**
hypersphere_volume = _other_math.hypersphere_volume
hypercube_volume = _other_math.hypercube_volume

# 🔢 **Randomized Math (From OtherMath)**
monte_carlo_pi = _other_math.monte_carlo_pi
random_walk = _other_math.random_walk
perlin_noise = _other_math.perlin_noise
fractal_dimension = _other_math.fractal_dimension

# 🔢 **4D Tesseract (From LeftMath)**
draw_tesseract = _left_math.draw_tesseract  # 🚀 Now ClawPy includes the 4D Simulation!



# 🔢 **MoreMath - Additional Tools**
distance_in_nD = _more_math.distance_in_nD
generate_random_graph = _more_math.generate_random_graph
fourier_transform = _more_math.fourier_transform
solve_equation_more = _more_math.solve_equation  # alias to avoid conflict
qr_decomposition = _more_math.qr_decomposition
matrix_eigenvalues = _more_math.matrix_eigenvalues
matrix_eigenvectors = _more_math.matrix_eigenvectors
matrix_inverse = _more_math.matrix_inverse
 
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
