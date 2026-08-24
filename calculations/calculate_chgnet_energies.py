from pathlib import Path
import csv

from chgnet.model.model import CHGNet
from pymatgen.core import Structure


# --------------------------------------------------
# 1. Define project folders
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

STRUCTURE_FOLDER = (
    PROJECT_ROOT
    / "structures"
    / "generated"
)

DATA_FOLDER = (
    PROJECT_ROOT
    / "data"
)

DATA_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# 2. Find all CIF files
# --------------------------------------------------

structure_files = sorted(
    STRUCTURE_FOLDER.glob("*.cif")
)

print()
print("Number of structures found:", len(structure_files))
print()


# --------------------------------------------------
# 3. Check that structures exist
# --------------------------------------------------

if len(structure_files) == 0:

    raise RuntimeError(
        "No CIF structures were found."
    )


# --------------------------------------------------
# 4. Load CHGNet ONCE
# --------------------------------------------------

print("Loading CHGNet model...")

model = CHGNet.load()

print("CHGNet model loaded successfully.")
print()


# --------------------------------------------------
# 5. Prepare result storage
# --------------------------------------------------

results = []


# --------------------------------------------------
# 6. Calculate energy for every structure
# --------------------------------------------------

for structure_number, structure_file in enumerate(
    structure_files,
    start=1
):

    print(
        f"Calculating structure "
        f"{structure_number}/{len(structure_files)}:"
    )

    print(structure_file.name)

    structure = Structure.from_file(
        structure_file
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


    # Count Al and Co atoms

    al_atoms = int(
        structure.composition["Al"]
    )

    co_atoms = int(
        structure.composition["Co"]
    )


    al_fraction = (
        al_atoms
        / number_of_atoms
    )

    co_fraction = (
        co_atoms
        / number_of_atoms
    )


    # Save the result

    results.append([
        structure_number,
        structure_file.name,
        number_of_atoms,
        al_atoms,
        co_atoms,
        al_fraction,
        co_fraction,
        energy_per_atom,
        total_energy
    ])


    print(
        f"Energy = "
        f"{energy_per_atom:.6f} eV/atom"
    )

    print()


# --------------------------------------------------
# 7. Save everything to CSV
# --------------------------------------------------

output_file = (
    DATA_FOLDER
    / "chgnet_energy_dataset.csv"
)


with open(
    output_file,
    "w",
    newline=""
) as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "structure_id",
        "filename",
        "total_atoms",
        "Al_atoms",
        "Co_atoms",
        "Al_fraction",
        "Co_fraction",
        "CHGNet_energy_eV_per_atom",
        "CHGNet_total_energy_eV"
    ])

    writer.writerows(results)


# --------------------------------------------------
# 8. Final message
# --------------------------------------------------

print("----------------------------------------")
print("ENERGY CALCULATION COMPLETED")
print("----------------------------------------")

print(
    "Number of structures calculated:",
    len(results)
)

print(
    "Dataset saved as:"
)

print(output_file)

print("----------------------------------------")