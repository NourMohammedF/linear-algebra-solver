"""
Linear Algebra Solver - Interactive Algebraic Structure Explorer

A comprehensive tool for exploring algebraic structures (groups, rings, fields)
over number sets (N, Z, Q, R) and 2x2 matrix sets (Mn, Gn, SLn, Kn).

Features:
- Number sets: N, Z, Q, R and variants (Z+, Z-, Z*, Q+, Q-, Q*, R+, R-, R*)
- Matrix sets: Mn (all 2x2), Gn (diagonal), SLn (det=1), Kn (identity)
- Operations: +, -, *, / (scalars) and ++, --, ** (matrices)
- Matrix operations: determinant, inverse, negation, equality
- Property checking: closure, associativity, identity, inverses, commutativity
- Classifies structures: magma, semigroup, monoid, group, abelian group
"""

from fractions import Fraction
import random
from typing import Any, Callable, List, Set, Union


# Type aliases
Matrix = List[List[Union[int, float, Fraction]]]
Scalar = Union[int, float, Fraction]
Element = Union[Scalar, Matrix]
Operation = Callable[[Element, Element], Element]


def is_valid_2x2_matrix(matrix: Any, allowed_entries: List = None) -> bool:
    """Check if input is a valid 2x2 matrix, optionally with allowed entries."""
    if not isinstance(matrix, list) or len(matrix) != 2:
        return False
    for row in matrix:
        if not isinstance(row, list) or len(row) != 2:
            return False
        if allowed_entries is not None:
            for entry in row:
                if entry not in allowed_entries:
                    return False
    return True


def is_valid_diagonal_matrix(matrix: Any, allowed_entries: List = None) -> bool:
    """Check if matrix is a valid 2x2 diagonal matrix."""
    if not is_valid_2x2_matrix(matrix, allowed_entries):
        return False
    return matrix[0][1] == 0 and matrix[1][0] == 0


def matrix_determinant(A: Matrix) -> Union[int, float, Fraction]:
    """Calculate determinant of 2x2 matrix."""
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def matrix_inverse(A: Matrix) -> Matrix:
    """Compute inverse of 2x2 matrix. Raises ValueError if not invertible."""
    det = matrix_determinant(A)
    if det == 0:
        raise ValueError("Matrix is not invertible (determinant is zero)")
    inv_det = 1 / det
    return [
        [A[1][1] * inv_det, -A[0][1] * inv_det],
        [-A[1][0] * inv_det, A[0][0] * inv_det]
    ]


def matrix_negate(A: Matrix) -> Matrix:
    """Return additive inverse (-A) of a 2x2 matrix."""
    return [[-A[i][j] for j in range(2)] for i in range(2)]


def matrices_equal(A: Matrix, B: Matrix) -> bool:
    """Check equality of two 2x2 matrices."""
    return all(A[i][j] == B[i][j] for i in range(2) for j in range(2))


def matrix_in_set(matrix: Matrix, matrix_set: List[Matrix]) -> bool:
    """Check if matrix is in the given set of matrices."""
    return any(matrices_equal(matrix, m) for m in matrix_set)


# Scalar operations
def add(a: Scalar, b: Scalar) -> Scalar:
    return a + b


def subtract(a: Scalar, b: Scalar) -> Scalar:
    return a - b


def multiply(a: Scalar, b: Scalar) -> Scalar:
    return a * b


def divide(a: Scalar, b: Scalar) -> Scalar:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b


# Matrix operations
def matrix_add(A: Matrix, B: Matrix) -> Matrix:
    if not (is_valid_2x2_matrix(A) and is_valid_2x2_matrix(B)):
        raise ValueError("Both arguments must be valid 2x2 matrices")
    return [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]


def matrix_subtract(A: Matrix, B: Matrix) -> Matrix:
    if not (is_valid_2x2_matrix(A) and is_valid_2x2_matrix(B)):
        raise ValueError("Both arguments must be valid 2x2 matrices")
    return [[A[i][j] - B[i][j] for j in range(2)] for i in range(2)]


def matrix_multiply(A: Matrix, B: Matrix) -> Matrix:
    if not (is_valid_2x2_matrix(A) and is_valid_2x2_matrix(B)):
        raise ValueError("Both arguments must be valid 2x2 matrices")
    return [
        [A[0][0] * B[0][0] + A[0][1] * B[1][0],
         A[0][0] * B[0][1] + A[0][1] * B[1][1]],
        [A[1][0] * B[0][0] + A[1][1] * B[1][0],
         A[1][0] * B[0][1] + A[1][1] * B[1][1]]
    ]


# Matrix set generators
def generate_Mn(n: int) -> List[Matrix]:
    """Generate all 2x2 matrices with entries from {-n+1, ..., n-1}."""
    matrices = []
    for i in range(-n + 1, n):
        for j in range(-n + 1, n):
            for k in range(-n + 1, n):
                for l in range(-n + 1, n):
                    matrices.append([[i, j], [k, l]])
    return matrices


def generate_Gn(n: int) -> List[Matrix]:
    """Generate 2x2 diagonal matrices with non-zero determinant."""
    matrices = []
    for i in range(-n + 1, n):
        for j in range(-n + 1, n):
            matrix = [[i, 0], [0, j]]
            if matrix_determinant(matrix) != 0:
                matrices.append(matrix)
    return matrices


def generate_SLn(n: int) -> List[Matrix]:
    """Generate 2x2 matrices with determinant = 1 (special linear group)."""
    matrices = []
    for i in range(-n + 1, n):
        for j in range(-n + 1, n):
            for k in range(-n + 1, n):
                for l in range(-n + 1, n):
                    matrix = [[i, j], [k, l]]
                    if matrix_determinant(matrix) == 1:
                        matrices.append(matrix)
    return matrices


def generate_Kn() -> List[Matrix]:
    """Generate set containing only the 2x2 identity matrix."""
    identity = [[1, 0], [0, 1]]
    return [identity]


# Property checkers
def check_closure(
    element_set: List[Element],
    operation: Operation,
    sample_size: int = 3,
    max_attempts: int = 10
) -> bool:
    """
    Check closure property using random sampling.
    Returns True if operation is closed on the set (within sample attempts).
    """
    if sample_size < 2 or sample_size > len(element_set):
        raise ValueError("Invalid sample_size. Must be between 2 and len(element_set).")

    for _ in range(max_attempts):
        sample = random.sample(element_set, sample_size)
        valid = True
        for a in sample:
            for b in sample:
                try:
                    result = operation(a, b)
                    if result not in element_set:
                        valid = False
                        break
                except (ValueError, ZeroDivisionError):
                    valid = False
                    break
            if not valid:
                break
        if valid:
            return True
    return False


def check_associativity(operation: Operation, test_range: range = range(-5, 6)) -> bool:
    """Check associativity: (a*b)*c == a*(b*c) for all a,b,c in test_range."""
    for a in test_range:
        for b in test_range:
            for c in test_range:
                try:
                    if operation(operation(a, b), c) != operation(a, operation(b, c)):
                        return False
                except (ValueError, ZeroDivisionError):
                    return False
    return True


def check_associativity_matrix(operation: Operation, matrices: List[Matrix]) -> bool:
    """Check associativity for matrix operations."""
    for A in matrices:
        for B in matrices:
            for C in matrices:
                try:
                    left = operation(operation(A, B), C)
                    right = operation(A, operation(B, C))
                    if not matrices_equal(left, right):
                        return False
                except (ValueError, ZeroDivisionError):
                    return False
    return True


def find_identity(element_set: List[Element], operation: Operation) -> Element:
    """Find identity element e such that a*e = e*a = a for all a in set."""
    for e in element_set:
        is_id = True
        for a in element_set:
            try:
                if operation(a, e) != a or operation(e, a) != a:
                    is_id = False
                    break
            except (ValueError, ZeroDivisionError):
                is_id = False
                break
        if is_id:
            return e
    return None


def find_identity_matrix(operation: Operation, matrices: List[Matrix]) -> Matrix:
    """Find identity matrix for matrix operations."""
    for E in matrices:
        is_id = True
        for A in matrices:
            try:
                if not (matrices_equal(operation(A, E), A) and matrices_equal(operation(E, A), A)):
                    is_id = False
                    break
            except (ValueError, ZeroDivisionError):
                is_id = False
                break
        if is_id:
            return E
    return None


def has_inverses(
    element_set: List[Element],
    operation: Operation,
    identity: Element
) -> bool:
    """Check if every element has an inverse in the set."""
    for a in element_set:
        found = False
        for b in element_set:
            try:
                if operation(a, b) == identity and operation(b, a) == identity:
                    found = True
                    break
            except (ValueError, ZeroDivisionError):
                continue
        if not found:
            return False
    return True


def has_inverses_matrix(
    matrices: List[Matrix],
    operation: Operation,
    identity: Matrix,
    operation_name: str
) -> bool:
    """Check if every matrix has an inverse in the set."""
    for A in matrices:
        found = False
        for B in matrices:
            try:
                if matrices_equal(operation(A, B), identity) and matrices_equal(operation(B, A), identity):
                    found = True
                    break
            except (ValueError, ZeroDivisionError):
                continue
        if not found:
            return False
    return True


def check_commutativity(
    element_set: List[Element],
    operation: Operation
) -> bool:
    """Check if operation is commutative: a*b == b*a for all a,b."""
    for a in element_set:
        for b in element_set:
            try:
                if operation(a, b) != operation(b, a):
                    return False
            except (ValueError, ZeroDivisionError):
                return False
    return True


def check_commutativity_matrix(
    matrices: List[Matrix],
    operation: Operation
) -> bool:
    """Check commutativity for matrix operations."""
    for A in matrices:
        for B in matrices:
            try:
                if not matrices_equal(operation(A, B), operation(B, A)):
                    return False
            except (ValueError, ZeroDivisionError):
                return False
    return True


def classify_structure(
    has_closure: bool,
    has_assoc: bool,
    has_identity: bool,
    has_inv: bool,
    is_commutative: bool
) -> str:
    """Classify the algebraic structure based on properties."""
    if not has_closure:
        return "Not a magma (closure fails)"
    if not has_assoc:
        return "Magma (closure only)"
    if not has_identity:
        return "Semigroup (closure + associativity)"
    if not has_inv:
        return "Monoid (closure + associativity + identity)"
    if is_commutative:
        return "Abelian Group (all properties + commutativity)"
    return "Group (closure + associativity + identity + inverses)"


def create_number_sets() -> dict:
    """Create all number sets used in the explorer."""
    natural = set(range(1, 50))
    integers = set(range(-30, 30))
    rational = set(Fraction(a, b) for a in range(-20, 20) for b in range(1, 20) if b != 0)
    real = set(float(i) / 100.0 for i in range(-100, 100) if i != 0)

    Z_pos = natural.copy()
    Z_neg = {x for x in integers if x < 0}
    Q_pos = {x for x in rational if x > 0}
    Q_neg = {x for x in rational if x < 0}
    R_pos = {x for x in real if x > 0}
    R_neg = {x for x in real if x < 0}

    return {
        'N': natural,
        'Z': integers | natural,
        'Q': rational | integers | natural,
        'R': real | rational | integers | natural | {0},
        'Z+': Z_pos,
        'Z-': Z_neg,
        'Z*': (integers | natural) - {0},
        'Q+': Q_pos | Z_pos,
        'Q-': Q_neg | Z_neg,
        'Q*': (rational | integers | natural) - {0},
        'R+': R_pos | Q_pos | Z_pos,
        'R-': R_neg | Q_neg | Z_neg,
        'R*': (real | rational | integers | natural) - {0},
    }


def create_matrix_sets() -> dict:
    """Create all matrix sets used in the explorer."""
    return {
        'MN': generate_Mn(5),
        'GN': generate_Gn(5),
        'SLN': generate_SLn(5),
        'KN': generate_Kn(),
    }


# Operation dictionaries
SCALAR_OPS = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
}

MATRIX_OPS = {
    '++': matrix_add,
    '--': matrix_subtract,
    '**': matrix_multiply,
}

ALL_OPS = {**SCALAR_OPS, **MATRIX_OPS}


def print_sets(sets: dict, filter_keys: List[str] = None):
    """Pretty print available sets."""
    keys = filter_keys if filter_keys else list(sets.keys())
    for key in keys:
        val = sets[key]
        if isinstance(val, set):
            sample = sorted(list(val))[:10]
            more = " ..." if len(val) > 10 else ""
            print(f"  {key}: {{{', '.join(str(x) for x in sample)}{more}}} ({len(val)} elements)")
        else:
            sample = val[:5]
            more = " ..." if len(val) > 5 else ""
            print(f"  {key}: [{', '.join(str(x) for x in sample)}{more}] ({len(val)} elements)")


def run_explorer():
    """Main interactive loop."""
    print("=" * 60)
    print("   Linear Algebra Solver - Algebraic Structure Explorer")
    print("=" * 60)

    number_sets = create_number_sets()
    matrix_sets = create_matrix_sets()
    all_sets = {**number_sets, **matrix_sets}

    while True:
        print("\n" + "-" * 60)
        print("MAIN MENU")
        print("-" * 60)
        print("1. Explore number sets (N, Z, Q, R and variants)")
        print("2. Explore matrix sets (Mn, Gn, SLn, Kn)")
        print("3. Quick test: classify a specific set/operation")
        print("4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == '1':
            explore_sets(number_sets, SCALAR_OPS, is_matrix=False)
        elif choice == '2':
            explore_sets(matrix_sets, MATRIX_OPS, is_matrix=True)
        elif choice == '3':
            quick_test(all_sets)
        elif choice == '4':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")


def explore_sets(sets: dict, ops: dict, is_matrix: bool):
    """Interactive exploration of a collection of sets."""
    print("\nAvailable sets:")
    print_sets(sets)

    set_key = input("\nEnter set name (or 'back'): ").strip().upper()
    if set_key == 'BACK':
        return
    if set_key not in sets:
        print(f"Unknown set: {set_key}")
        return

    print("\nAvailable operations:")
    for sym in ops:
        print(f"  {sym}")

    op_key = input("\nEnter operation symbol: ").strip()
    if op_key not in ops:
        print(f"Unknown operation: {op_key}")
        return

    chosen_set = list(sets[set_key])
    chosen_op = ops[op_key]

    print(f"\nAnalyzing ({set_key}, {op_key})...")
    print("-" * 40)

    # Check properties
    print("Checking closure...")
    try:
        closure = check_closure(chosen_set, chosen_op)
        print(f"  Closure: {'✓' if closure else '✗'}")
    except Exception as e:
        print(f"  Closure check failed: {e}")
        closure = False

    if closure:
        print("Checking associativity...")
        if is_matrix:
            assoc = check_associativity_matrix(chosen_op, chosen_set)
        else:
            assoc = check_associativity(chosen_op)
        print(f"  Associativity: {'✓' if assoc else '✗'}")
    else:
        assoc = False

    identity = None
    has_inv = False
    commutative = False

    if closure and assoc:
        print("Checking identity...")
        if is_matrix:
            identity = find_identity_matrix(chosen_op, chosen_set)
        else:
            identity = find_identity(chosen_set, chosen_op)
        has_id = identity is not None
        print(f"  Identity: {'✓' if has_id else '✗'} ({identity})")

        if has_id:
            print("Checking inverses...")
            if is_matrix:
                has_inv = has_inverses_matrix(chosen_set, chosen_op, identity, op_key)
            else:
                has_inv = has_inverses(chosen_set, chosen_op, identity)
            print(f"  Inverses: {'✓' if has_inv else '✗'}")

            print("Checking commutativity...")
            if is_matrix:
                commutative = check_commutativity_matrix(chosen_set, chosen_op)
            else:
                commutative = check_commutativity(chosen_set, chosen_op)
            print(f"  Commutativity: {'✓' if commutative else '✗'}")
    else:
        has_id = False

    # Classification
    structure = classify_structure(closure, assoc, has_id, has_inv, commutative)
    print(f"\n>>> Structure: {structure}")

    # Offer to test another
    if input("\nTest another? (y/n): ").lower().startswith('y'):
        explore_sets(sets, ops, is_matrix)


def quick_test(all_sets: dict):
    """Quick classification test for any set/operation combination."""
    print("\nAll available sets:")
    print_sets(all_sets)

    print("\nAll operations:")
    for sym in ALL_OPS:
        print(f"  {sym}")

    set_key = input("\nSet name: ").strip().upper()
    op_key = input("Operation: ").strip()

    if set_key not in all_sets or op_key not in ALL_OPS:
        print("Invalid set or operation.")
        return

    is_matrix = set_key in ['MN', 'GN', 'SLN', 'KN']
    chosen_set = list(all_sets[set_key])
    chosen_op = ALL_OPS[op_key]

    print(f"\nQuick classification of ({set_key}, {op_key})...")
    print("-" * 40)

    try:
        closure = check_closure(chosen_set, chosen_op)
        assoc = check_associativity_matrix(chosen_op, chosen_set) if is_matrix else check_associativity(chosen_op)
        identity = find_identity_matrix(chosen_op, chosen_set) if is_matrix else find_identity(chosen_set, chosen_op)
        has_id = identity is not None
        has_inv = (has_inverses_matrix(chosen_set, chosen_op, identity, op_key) if is_matrix
                   else has_inverses(chosen_set, chosen_op, identity)) if has_id else False
        commutative = (check_commutativity_matrix(chosen_set, chosen_op) if is_matrix
                       else check_commutativity(chosen_set, chosen_op)) if has_id else False

        print(f"Closure: {'✓' if closure else '✗'}")
        print(f"Associativity: {'✓' if assoc else '✗'}")
        print(f"Identity: {'✓' if has_id else '✗'} ({identity})")
        print(f"Inverses: {'✓' if has_inv else '✗'}")
        print(f"Commutativity: {'✓' if commutative else '✗'}")
        print(f"\n>>> {classify_structure(closure, assoc, has_id, has_inv, commutative)}")

    except Exception as e:
        print(f"Error during analysis: {e}")


if __name__ == "__main__":
    run_explorer()