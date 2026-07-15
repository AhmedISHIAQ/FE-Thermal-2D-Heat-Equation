# 2D Finite Element Solver for Stationary Thermal Problems

This project implements a small finite element solver in Python for two-dimensional stationary thermal conduction problems.

The project was completed as part of a Numerical Methods finite element lab. The main objective was to complete the missing element-level routines for a 3-node triangular finite element and validate the implementation using analytical solutions.

The code solves stationary heat conduction problems of the form:

```math
-\nabla \cdot (K \nabla u) = r
```

where:

- `u` is the unknown temperature field,
- `K` is the thermal conductivity,
- `r` is a source term.

The solver supports:

- 2D domains,
- 3-node linear triangular elements,
- isotropic thermal conductivity,
- Dirichlet boundary conditions,
- Neumann boundary conditions,
- constant or spatially varying source terms,
- Gmsh `.msh` mesh files,
- Gmsh `.pos` output files for visualization.

---

## 1. Project Objective

The objective of this project is to understand and complete a simple finite element code for stationary thermal analysis.

The missing routines were implemented in:

```text
tri3ThermalDirect.py
```

The completed routines are:

| Function | Purpose |
|---|---|
| `computeKe` | Computes the elementary stiffness matrix |
| `computeFve` | Computes the elementary source/load vector |
| `computeFNe` | Computes the elementary Neumann boundary force vector |

---

## 2. Governing Equation

The stationary heat equation is:

```math
-\nabla \cdot (K \nabla u) = r
```

For isotropic conductivity, `K` is a scalar.

The weak form is:

```math
\int_{\Omega} K \nabla v \cdot \nabla u \, d\Omega
=
\int_{\Omega} v r \, d\Omega
+
\int_{\Gamma_N} v q_N \, d\Gamma
```

This leads to the finite element linear system:

```math
\mathbf{K}\mathbf{U} = \mathbf{F}
```

where:

- `K` is the global stiffness matrix,
- `U` is the vector of unknown nodal temperatures,
- `F` is the global force vector.

---

## 3. Finite Element Used

The solver uses a 3-node linear triangular element.

For one triangular element, the temperature is approximated as:

```math
u_h(x,y) = N_1 u_1 + N_2 u_2 + N_3 u_3
```

where:

- `N1`, `N2`, and `N3` are the linear shape functions,
- `u1`, `u2`, and `u3` are the nodal temperatures.

For a linear triangular element, the shape function gradients are constant inside each element.

The elementary stiffness matrix is:

```math
\mathbf{K}_e = K A_e \mathbf{B}^T \mathbf{B}
```

where:

- `Ae` is the area of the triangular element,
- `B` is the matrix containing the derivatives of the shape functions.

---

## 4. Project Structure

```text
FE_Thermal_2D/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── solveFE.py
├── tri3ThermalDirect.py
├── testFE.py
├── gmshParser.py
├── export.py
├── integrationRule.py
├── sparseUtils.py
│
├── validate_element_routines.py
├── run_linear_validation.py
├── run_source_validation.py
├── check_source_error.py
│
├── meshes/
│   ├── square2x2.msh
│   ├── square4x4.msh
│   ├── square10x10.msh
│   ├── square20x20.msh
│   └── ...
│
├── results/
│   ├── temperature.pos
│   └── validation_results.txt
│
└── docs/
    └── finite_element_project_explanation.pdf
```

---

## 5. Description of Main Files

| File | Description |
|---|---|
| `testFE.py` | Defines the problem to solve: mesh, material property, source term, boundary conditions, and output name |
| `solveFE.py` | Main finite element solver. It reads the mesh, assembles the system, applies boundary conditions, solves, and exports the result |
| `tri3ThermalDirect.py` | Contains the triangular element routines implemented in this project |
| `gmshParser.py` | Reads Gmsh `.msh` mesh files |
| `export.py` | Exports the computed temperature field to a `.pos` file |
| `integrationRule.py` | Contains numerical integration rules |
| `sparseUtils.py` | Contains helper functions for sparse matrix assembly |
| `validate_element_routines.py` | Tests the elementary stiffness matrix and force vectors |
| `run_linear_validation.py` | Runs a validation problem with a known linear analytical solution |
| `run_source_validation.py` | Runs a validation problem with a source term and zero boundary temperature |
| `check_source_error.py` | Compares the numerical solution with the analytical Fourier-series solution |

---

## 6. Boundary and Domain Physical IDs

The square mesh uses physical IDs to identify boundaries and the domain.

| Physical ID | Meaning |
|---:|---|
| `101` | Bottom boundary |
| `102` | Right boundary |
| `103` | Top boundary |
| `104` | Left boundary |
| `1000` | Square domain |

For example:

```python
BCD_lns = {101: 0.0}
```

means that a Dirichlet boundary condition is applied on the bottom boundary.

```python
BCNs = {103: 1.0}
```

means that a Neumann flux is applied on the top boundary.

---

## 7. Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/FE_Thermal_2D.git
cd FE_Thermal_2D
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Required packages:

```text
numpy
scipy
```

If plotting scripts are added later, `matplotlib` may also be required.

---

## 8. How to Run the Main Example

Run:

```bash
python testFE.py
```

This generates a Gmsh result file:

```text
temperature.pos
```

The file can be opened in Gmsh to visualize the computed temperature field.

---

## 9. How to View the Mesh

To view a mesh file, open Gmsh and load one of the `.msh` files.

Example:

```bash
gmsh meshes/square20x20.msh
```

Alternatively:

1. Open Gmsh.
2. Click `File`.
3. Click `Open`.
4. Select a `.msh` file.

---

## 10. How to View the Temperature Result

After running the solver, open the generated `.pos` file in Gmsh.

Example:

```bash
gmsh results/temperature.pos
```

or:

```bash
gmsh temperature.pos
```

depending on where the output file is saved.

In Gmsh, the temperature field is shown as a colored scalar field.

---

## 11. Validation 1: Element-Level Test

The first validation checks the elementary routines directly.

Run:

```bash
python validate_element_routines.py
```

For the reference triangle:

```text
(0,0), (1,0), (0,1)
```

with unit conductivity, the expected elementary stiffness matrix is:

```text
[[ 1.  -0.5 -0.5]
 [-0.5  0.5  0. ]
 [-0.5  0.   0.5]]
```

For a unit source term on the same triangle, the expected volume force vector is:

```text
[0.16666667 0.16666667 0.16666667]
```

For a unit flux on a unit edge, the expected Neumann force vector is:

```text
[0.5 0.5]
```

These results confirm that the element-level implementation is correct.

---

## 12. Validation 2: Linear Analytical Solution

The second validation uses a simple problem with a known linear exact solution.

The problem is:

```math
r = 0
```

with a prescribed temperature on the bottom boundary and a flux on the top boundary.

The analytical solution is linear:

```math
u(y) = \frac{q_N}{K}(y + 1)
```

For:

```text
qN = 1
K = 1
```

the exact solution becomes:

```math
u(y) = y + 1
```

This means:

- at `y = -1`, `u = 0`,
- at `y = 0`, `u = 1`,
- at `y = 1`, `u = 2`.

Run:

```bash
python run_linear_validation.py
```

Since the exact solution is linear, the 3-node triangular element should reproduce it almost exactly.

---

## 13. Validation 3: Source Problem with Analytical Solution

The third validation solves:

```math
-\Delta u = 1
```

on the square domain:

```math
[-1,1] \times [-1,1]
```

with:

```math
u = 0
```

on all boundaries.

Run:

```bash
python run_source_validation.py
```

The expected result is:

- zero temperature on all boundaries,
- maximum temperature at the center,
- symmetry about the horizontal and vertical axes.

The analytical solution is given by a Fourier sine series. The script:

```bash
python check_source_error.py
```

compares the numerical solution with the analytical solution and checks that the error decreases when the mesh is refined.

---

## 14. Expected Validation Behavior

For the linear validation problem:

```text
The numerical error should be close to machine precision.
```

For the source problem:

```text
The error should decrease as the mesh is refined.
```

Example behavior:

| Mesh | Expected behavior |
|---|---|
| `square4x4.msh` | Larger error |
| `square10x10.msh` | Smaller error |
| `square20x20.msh` | Even smaller error |
| `square40x40.msh` | Smallest error |

This confirms that the finite element implementation is converging correctly.

---

## 15. Notes on Generated Files

The solver generates `.pos` files for visualization in Gmsh.

These files are output files, so they may be ignored in Git unless a sample result is intentionally included.

Recommended approach:

- Keep source code and validation scripts in the repository.
- Keep one sample result file in `results/`.
- Ignore other generated `.pos` files.

Example `.gitignore` rule:

```gitignore
*.pos
!results/temperature.pos
```

---

## 16. Documentation

A detailed explanation of the finite element formulation, implementation, and validation is included in:

```text
docs/finite_element_project_explanation.pdf
```

This document explains the mathematical formulation, the implemented routines, the validation problems, and the interpretation of the results.

---

## 17. Summary

This project completes and validates a small 2D finite element solver for stationary thermal conduction problems.

The main achievements are:

- implementation of the triangular element stiffness matrix,
- implementation of the source force vector,
- implementation of the Neumann boundary force vector,
- validation using element-level tests,
- validation using a linear analytical solution,
- validation using a source problem with known analytical solution,
- visualization of the numerical results using Gmsh.

---

## 18. Author

Prepared by:

```text
YOUR NAME
```

Course:

```text
Numerical Methods / Finite Element Lab
```