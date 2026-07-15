from solveFE import solveFE


meshName = "square20x20.msh"

BCNs = {}

# Zero temperature on all four boundaries
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

# Constant source term r = 1
sourceTerm = lambda xyz, physElt: 1.0

exportName = "source_validation.pos"

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