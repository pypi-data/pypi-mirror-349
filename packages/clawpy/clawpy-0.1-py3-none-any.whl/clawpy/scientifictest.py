#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "./")
from scientific import ScientificMath

# Create an instance of ScientificMath
sci_math = ScientificMath()

print("\n **Scientific Math Tests**")

# Thermodynamics Tests
print("\n **Thermodynamics**")
print("Heat Transfer (m=2 kg, c=4.18 J/g°C, delta_T=10°C):", sci_math.heat_transfer(2, 4.18, 10))
print("Entropy Change (Q=500 J, T=300 K):", sci_math.entropy_change(500, 300))
print("Ideal Gas Law (P=101325 Pa, V=0.0224 m^3, n=1 mol):", sci_math.ideal_gas_law(101325, 0.0224, 1))

# Quantum Mechanics Tests
print("\n **Quantum Mechanics**")
print("Wave Energy (f=5e14 Hz):", sci_math.wave_energy(5e14))
print("Schrodinger Energy (n=1, m=9.109e-31 kg, L=1e-9 m):", sci_math.schrodinger_energy(1, 9.109e-31, 1e-9))

# Chemistry Tests
print("\n **Chemistry**")
elements = ["H", "O"]
amounts = [2, 1]  # H2O
print("Molecular Weight of H2O:", sci_math.molecular_weight(elements, amounts))
print("Reaction Rate (k=0.1, concentrations=[0.5, 0.2], orders=[1, 2]):", sci_math.reaction_rate(0.1, [0.5, 0.2], [1, 2]))

# Astronomy Tests
print("\n **Astronomy**")
earth_mass = 5.972e24  # kg
earth_radius = 6.371e6  # m
print("Orbital Velocity (Earth mass, Earth radius):", sci_math.orbital_velocity(earth_mass, earth_radius))
print("Escape Velocity (Earth mass, Earth radius):", sci_math.escape_velocity(earth_mass, earth_radius))
