import numpy as np
from solveFE import solveFE


def read_pos_solution(filename):
    """
    Read node coordinates and nodal values from a .pos file exported by this solver.
    """

    with open(filename, "r") as file:
        lines = file.readlines()

    # Read nodes
    node_start = lines.index("$Nodes\n")
    n_nodes = int(lines[node_start + 1])

    coords = np.zeros((n_nodes, 3))

    for i in range(n_nodes):
        parts = lines[node_start + 2 + i].split()
        node_id = int(parts[0]) - 1
        coords[node_id, 0] = float(parts[1])
        coords[node_id, 1] = float(parts[2])
        coords[node_id, 2] = float(parts[3])

    # Read nodal solution values
    data_start = lines.index("$NodeData\n")

    # In this file format, number of node values appears 9 lines after $NodeData
    value_count_line = data_start + 9
    n_values = int(lines[value_count_line])

    values = np.zeros(n_values)

    for i in range(n_values):
        parts = lines[value_count_line + 1 + i].split()
        node_id = int(parts[0]) - 1
        values[node_id] = float(parts[1])

    return coords, values


def exact_solution_source_square(x, y, n_terms=51):
    """
    Analytical solution of:
        -Delta u = 1
    on:
        [-1,1] x [-1,1]
    with:
        u = 0 on all boundaries.
    """

    value = 0.0

    for i in range(1, n_terms + 1, 2):
        for j in range(1, n_terms + 1, 2):

            coeff = 64.0 / (
                np.pi**4 * (i**2 + j**2) * i * j
            )

            value += coeff \
                * np.sin(i * np.pi * (x + 1.0) / 2.0) \
                * np.sin(j * np.pi * (y + 1.0) / 2.0)

    return value


def run_case(meshName):

    outputName = meshName.replace(".msh", "_source_validation.pos")

    BCNs = {}

    BCD_lns = {
        101: 0.0,
        102: 0.0,
        103: 0.0,
        104: 0.0
    }

    BCD_nds = {}

    conductivities = {
        1000: 1.0
    }

    sourceTerm = lambda xyz, physElt: 1.0

    solveFE(
        meshName,
        conductivities,
        BCNs,
        BCD_lns,
        BCD_nds,
        sourceTerm,
        outputName,
        useSparse=False,
        verboseOutput=False
    )

    coords, numerical = read_pos_solution(outputName)

    exact = np.zeros_like(numerical)

    for i in range(len(numerical)):
        x = coords[i, 0]
        y = coords[i, 1]
        exact[i] = exact_solution_source_square(x, y)

    error = np.abs(numerical - exact)
    max_error = np.max(error)

    print(meshName, "max nodal error =", max_error)


meshes = [
    "square4x4.msh",
    "square10x10.msh",
    "square20x20.msh",
    "square30x30.msh",
    "square40x40.msh"
]

for meshName in meshes:
    run_case(meshName)