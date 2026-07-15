from solveFE import solveFE


meshName = "square20x20.msh"

K = 1.0
qN = 1.0

# Unit flux on top boundary
BCNs = {
    103: qN
}

# Temperature fixed to zero on bottom boundary
BCD_lns = {
    101: 0.0
}

# No point Dirichlet BCs needed because bottom line is fixed
BCD_nds = {}

# Conductivity in the square domain
conductivities = {
    1000: K
}

# No source term
sourceTerm = lambda xyz, physElt: 0.0

exportName = "linear_validation.pos"

useSparse = False
verboseOutput = False

solveFE(
    meshName,
    conductivities,
    BCNs,
    BCD_lns,
    BCD_nds,
    sourceTerm,
    exportName,
    useSparse,
    verboseOutput
)