# MIT License © 2025 Anish Chaudhuri
# See full license at the bottom of this file.

import numpy as np
import math

class ScientificMath:
    def __init__(self):
        pass

    # 🔥 THERMODYNAMICS
    def heat_transfer(self, mass, specific_heat, temp_change):
        """Calculates heat transfer using Q = mcΔT."""
        return mass * specific_heat * temp_change

    def entropy_change(self, heat, temp):
        """Calculates entropy change using ΔS = Q / T."""
        return heat / temp if temp != 0 else "Undefined"

    def ideal_gas_law(self, pressure, volume, moles, R=8.314):
        """Calculates temperature using PV = nRT."""
        return (pressure * volume) / (moles * R)

    # ⚛️ QUANTUM MECHANICS
    def wave_energy(self, frequency):
        """Calculates energy of a wave using E = h * f."""
        h = 6.626e-34  # Planck’s constant
        return h * frequency

    def schrodinger_energy(self, n, mass, length):
        """Calculates energy levels in a quantum box using E_n = (n^2 * h^2) / (8mL^2)."""
        h = 6.626e-34  # Planck’s constant
        return (n**2 * h**2) / (8 * mass * length**2)

    # 🧪 CHEMISTRY
    def molecular_weight(self, elements, amounts):
        """Calculates molecular weight given elements and their amounts."""
        atomic_weights = {
            "H": 1.008, "C": 12.011, "O": 15.999, "N": 14.007, "Na": 22.990,
            "Cl": 35.45, "Fe": 55.845, "S": 32.065, "P": 30.974
        }
        return sum(atomic_weights[e] * a for e, a in zip(elements, amounts) if e in atomic_weights)

    def reaction_rate(self, k, concentrations, orders):
        """Calculates reaction rate using rate = k * [A]^m * [B]^n ..."""
        return k * np.prod([conc**order for conc, order in zip(concentrations, orders)])

    # 🌌 ASTRONOMY
    def orbital_velocity(self, mass, radius):
        """Calculates orbital velocity using v = sqrt(GM/R)."""
        G = 6.67430e-11  # Gravitational constant
        return np.sqrt(G * mass / radius)

    def escape_velocity(self, mass, radius):
        """Calculates escape velocity using v = sqrt(2GM/R)."""
        G = 6.67430e-11  # Gravitational constant
        return np.sqrt(2 * G * mass / radius)

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
