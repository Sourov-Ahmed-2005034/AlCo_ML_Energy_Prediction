from pathlib import Path
import csv

from chgnet.model.model import CHGNet
from pymatgen.core import Structure


# --------------------------------------------------
# 1. Define folders
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REFERENCE_FOLDER = (
    PROJECT_ROOT
    / "structures"
    / "references"
)

DATA_FOLDER = (
    PROJECT_ROOT
    / "data"
)


# --------------------------------------------------
# 2. Reference files
# --------------------------------------------------

reference_files = {
    "Al": REFERENCE_FOLDER / "pure_Al_fcc.cif",
    "Co": REFERENCE_FOLDER / "pure_Co_fcc.cif"
}


# --------------------------------------------------
# 3. Load CHGNet
# --------------------------------------------------

print()
print("Loading CHGNet...")

model = CHGNet.load()

print("CHGNet loaded successfully.")
print()


# --------------------------------------------------
# 4. Calculate elemental energies
# --------------------------------------------------

results = []


for element, filepath in reference_files.items():

    print(
        "Calculating reference energy for",
        element
    )

    structure = Structure.from_file(
        filepath
    )

    prediction = model.predict_structure(
        structure,
        task="e"
    )

    energy_per_atom = float(
        prediction["e"].item()
    )

    number_of_atoms = len(structure)

    total_energy = (
        energy_per_atom
        * number_of_atoms
    )

    results.append([
        element,
        filepath.name,
        number_of_atoms,
        energy_per_atom,
        total_energy
    ])

    print(
        f"{element} energy = "
        f"{energy_per_atom:.6f} eV/atom"
    )

    print()


# --------------------------------------------------
# 5. Save reference energies
# --------------------------------------------------

output_file = (
    DATA_FOLDER
    / "chgnet_reference_energies.csv"
)


with open(
    output_file,
    "w",
    newline=""
) as csvfile:

    writer = csv.writer(
        csvfile
    )

    writer.writerow([
        "element",
        "filename",
        "number_of_atoms",
        "energy_eV_per_atom",
        "total_energy_eV"
    ])

    writer.writerows(
        results
    )


print("----------------------------------------")
print("REFERENCE ENERGY CALCULATION COMPLETE")
print("----------------------------------------")

print(
    "Saved as:",
    output_file
)

print("----------------------------------------")