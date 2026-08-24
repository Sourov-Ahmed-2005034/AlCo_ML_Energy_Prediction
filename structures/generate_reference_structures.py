from pathlib import Path

from ase.build import bulk
from ase.io import write


# --------------------------------------------------
# 1. Define project folders
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REFERENCE_FOLDER = (
    PROJECT_ROOT
    / "structures"
    / "references"
)

REFERENCE_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# 2. Create pure FCC aluminum
# --------------------------------------------------

# Approximate room-temperature FCC lattice parameter
# used only as the starting geometry for this demonstration.

al = bulk(
    "Al",
    "fcc",
    a=4.05,
    cubic=True
)

al = al * (2, 2, 2)


# --------------------------------------------------
# 3. Create pure FCC cobalt
# --------------------------------------------------

# Co is HCP in its equilibrium ground state,
# but we deliberately use FCC Co because our
# 21 Al-Co configurations are FCC-based.
#
# This means our later result is an
# FCC-constrained formation/mixing-energy estimate.

co = bulk(
    "Co",
    "fcc",
    a=3.54,
    cubic=True
)

co = co * (2, 2, 2)


# --------------------------------------------------
# 4. Save structures
# --------------------------------------------------

al_file = (
    REFERENCE_FOLDER
    / "pure_Al_fcc.cif"
)

co_file = (
    REFERENCE_FOLDER
    / "pure_Co_fcc.cif"
)


write(
    al_file,
    al
)

write(
    co_file,
    co
)


# --------------------------------------------------
# 5. Report result
# --------------------------------------------------

print()
print("----------------------------------------")
print("REFERENCE STRUCTURES CREATED")
print("----------------------------------------")

print(
    "Pure Al atoms:",
    len(al)
)

print(
    "Pure Co atoms:",
    len(co)
)

print()
print(
    "Al saved as:",
    al_file
)

print(
    "Co saved as:",
    co_file
)

print("----------------------------------------")