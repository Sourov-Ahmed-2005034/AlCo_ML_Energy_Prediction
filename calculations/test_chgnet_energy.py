from pathlib import Path

from chgnet.model.model import CHGNet
from pymatgen.core import Structure


# --------------------------------------------------
# 1. Find the main project folder
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]


# --------------------------------------------------
# 2. Select ONE Al-Co structure
# --------------------------------------------------

structure_file = (
    PROJECT_ROOT
    / "structures"
    / "generated"
    / "AlCo_10_Al0.500_seed1.cif"
)


print("Reading structure:")
print(structure_file)
print()


# --------------------------------------------------
# 3. Read the CIF structure
# --------------------------------------------------

structure = Structure.from_file(structure_file)

print("Structure loaded successfully.")
print("Number of atoms:", len(structure))
print("Composition:", structure.composition)
print()


# --------------------------------------------------
# 4. Load pretrained CHGNet model
# --------------------------------------------------

print("Loading CHGNet model...")

model = CHGNet.load()

print("CHGNet model loaded.")
print()


# --------------------------------------------------
# 5. Predict energy
# --------------------------------------------------

print("Calculating energy...")

prediction = model.predict_structure(
    structure,
    task="e"
)


# CHGNet returns energy in eV/atom
energy_per_atom = float(prediction["e"].item())

total_energy = energy_per_atom * len(structure)


# --------------------------------------------------
# 6. Print results
# --------------------------------------------------

print()
print("----------------------------------------")
print("CHGNet ENERGY RESULT")
print("----------------------------------------")

print("Energy per atom:", energy_per_atom, "eV/atom")
print("Total energy:", total_energy, "eV")

print("----------------------------------------")