# Linear Algebra Solver

An interactive Python tool for exploring algebraic structures (groups, rings, fields) over number sets and 2×2 matrix sets.

## Features

### Number Sets
- **N** — Natural numbers (1–49)
- **Z** — Integers (−29 to 29)
- **Q** — Rational numbers (fractions ±20/±20)
- **R** — Real numbers (floats ±1.00)
- **Variants**: Z⁺, Z⁻, Z*, Q⁺, Q⁻, Q*, R⁺, R⁻, R* (positive, negative, non-zero)

### Matrix Sets (2×2)
- **Mn** — All matrices with entries in {−4, −3, ..., 3, 4}
- **Gn** — Diagonal matrices with non-zero determinant
- **SLn** — Special linear group (determinant = 1)
- **Kn** — Identity matrix only

### Operations
| Scalar | Matrix |
|--------|--------|
| `+` add | `++` add |
| `-` subtract | `--` subtract |
| `*` multiply | `**` multiply |
| `/` divide | |

### Matrix Functions
- `determinant(A)` — determinant of 2×2 matrix
- `inverse(A)` — inverse of 2×2 matrix (raises if singular)
- `negate(A)` — additive inverse (−A)
- `equal(A, B)` — matrix equality

### Algebraic Properties Checked
1. **Closure** — a ★ b ∈ S for all a, b ∈ S
2. **Associativity** — (a ★ b) ★ c = a ★ (b ★ c)
3. **Identity** — ∃e: a ★ e = e ★ a = a
4. **Inverses** — ∀a ∃b: a ★ b = b ★ a = e
5. **Commutativity** — a ★ b = b ★ a

### Structure Classification
- **Magma** — closure only
- **Semigroup** — closure + associativity
- **Monoid** — semigroup + identity
- **Group** — monoid + inverses
- **Abelian Group** — group + commutativity

## Quick Start

```bash
python linear_algebra_solver.py
```

## Example Session

```
>>> Set: Z* (non-zero integers), Operation: * (multiplication)
Closure: ✓
Associativity: ✓
Identity: ✓ (1)
Inverses: ✗ (no multiplicative inverses in Z*)
Commutativity: ✓
>>> Structure: Monoid (closure + associativity + identity)

>>> Set: SLn (det=1 matrices), Operation: ** (matrix multiplication)
Closure: ✓
Associativity: ✓
Identity: ✓ ([[1,0],[0,1]])
Inverses: ✓
Commutativity: ✗
>>> Structure: Group (closure + associativity + identity + inverses)
```

## Requirements
- Python 3.8+
- Standard library only (`fractions`, `random`, `typing`)

## License
MIT