import numpy as np


# Computation of the elementary stiffness matrix Ke
# xyzVerts (INPUT): Coordinates of the nodes of the element (3x3 numpy array)
# conductivity (INPUT): Conductivity on the current element (scalar number)
# Ke (OUTPUT): Elementary stiffness matrix (3x3 numpy array)
def computeKe(xyzVerts, conductivity):

    # Coordinates of the three triangle nodes
    x1, y1 = xyzVerts[0, 0], xyzVerts[0, 1]
    x2, y2 = xyzVerts[1, 0], xyzVerts[1, 1]
    x3, y3 = xyzVerts[2, 0], xyzVerts[2, 1]

    # Area of the triangle
    A = 0.5 * abs(
        x1 * (y2 - y3)
        + x2 * (y3 - y1)
        + x3 * (y1 - y2)
    )

    # Coefficients used to compute the derivatives of the shape functions
    b1 = y2 - y3
    b2 = y3 - y1
    b3 = y1 - y2

    c1 = x3 - x2
    c2 = x1 - x3
    c3 = x2 - x1

    # Gradient matrix B
    B = (1.0 / (2.0 * A)) * np.array([
        [b1, b2, b3],
        [c1, c2, c3]
    ])

    # Elementary stiffness matrix
    Ke = conductivity * A * (B.T @ B)

    return Ke


# Computation of the elementary volume force vector Fve
# xyzVerts (INPUT): Coordinates of the nodes of the element (3x3 numpy array)
# sourceTerm (INPUT): Source term evaluator
# physElt (INPUT): physical id of the current element
# Fve (OUTPUT): Elementary force vector (3 components numpy array)
def computeFve(xyzVerts, sourceTerm, physElt):

    # Coordinates of the three triangle nodes
    x1, y1 = xyzVerts[0, 0], xyzVerts[0, 1]
    x2, y2 = xyzVerts[1, 0], xyzVerts[1, 1]
    x3, y3 = xyzVerts[2, 0], xyzVerts[2, 1]

    # Area of the triangle
    A = 0.5 * abs(
        x1 * (y2 - y3)
        + x2 * (y3 - y1)
        + x3 * (y1 - y2)
    )

    # Centroid of the triangle
    xyzCentroid = (xyzVerts[0, :] + xyzVerts[1, :] + xyzVerts[2, :]) / 3.0

    # Evaluate the source term at the centroid
    r = sourceTerm(xyzCentroid, physElt)

    # For a linear triangular element:
    # integral(N1)dA = A/3
    # integral(N2)dA = A/3
    # integral(N3)dA = A/3
    Fve = r * A / 3.0 * np.ones(3)

    return Fve


# Computation of the elementary Neumann force vector FNe
# xyzVerts (INPUT): Coordinates of the nodes of the edge (2x3 numpy array)
# flux (INPUT): Value of the prescribed flux on the current edge
# FNe (OUTPUT): Elementary force vector (2 components numpy array)
def computeFNe(xyzVerts, flux):

    # Coordinates of the two edge nodes
    x1, y1 = xyzVerts[0, 0], xyzVerts[0, 1]
    x2, y2 = xyzVerts[1, 0], xyzVerts[1, 1]

    # Length of the boundary edge
    L = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # For a linear edge element:
    # integral(N1)dL = L/2
    # integral(N2)dL = L/2
    FNe = flux * L / 2.0 * np.ones(2)

    return FNe