import numpy as np
from tri3ThermalDirect import computeKe, computeFve, computeFNe


# ------------------------------------------------------------
# Test 1: elementary stiffness matrix
# ------------------------------------------------------------

xyz_triangle = np.array([
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0]
])

conductivity = 1.0

Ke = computeKe(xyz_triangle, conductivity)

print("Elementary stiffness matrix Ke:")
print(Ke)


# ------------------------------------------------------------
# Test 2: elementary volume force vector
# ------------------------------------------------------------

sourceTerm = lambda xyz, physElt: 1.0

Fve = computeFve(xyz_triangle, sourceTerm, 1000)

print("\nElementary volume force vector Fve:")
print(Fve)


# ------------------------------------------------------------
# Test 3: elementary Neumann force vector
# ------------------------------------------------------------

xyz_edge = np.array([
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0]
])

flux = 1.0

FNe = computeFNe(xyz_edge, flux)

print("\nElementary Neumann force vector FNe:")
print(FNe)