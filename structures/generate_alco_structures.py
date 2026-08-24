from pathlib import Path
import random
import csv

from ase.build import bulk
from ase.io import write


# --------------------------------------------------
# 1. Find project folders automatically
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_FOLDER = PROJECT_ROOT / "structures" / "generated"
DATA_FOLDER = PROJECT_ROOT / "data"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
DATA_FOLDER.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Create a 2 x 2 x 2 FCC supercell
# --------------------------------------------------

base_structure = bulk(
    "Al",
    "fcc",
    a=4.05,
    cubic=True
)

base_structure = base_structure * (2, 2, 2)

number_of_atoms = len(base_structure)

print("Number of atoms in each structure:", number_of_atoms)


# --------------------------------------------------
# 3. Al compositions that we want
# --------------------------------------------------

al_fractions = [
    0.125,
    0.250,
    0.375,
    0.500,
    0.625,
    0.750,
    0.875
]


# Three different random arrangements for each composition
random_seeds = [
    1,
    2,
    3
]


# --------------------------------------------------
# 4. Generate structures
# --------------------------------------------------

metadata = []

structure_number = 1


for al_fraction in al_fractions:

    number_of_al = round(al_fraction * number_of_atoms)
    number_of_co = number_of_atoms - number_of_al

    actual_al_fraction = number_of_al / number_of_atoms
    actual_co_fraction = number_of_co / number_of_atoms

    for seed in random_seeds:

        atoms = base_structure.copy()

        # Start with all atoms as Al
        symbols = ["Al"] * number_of_atoms

        # Randomly choose which positions will become Co
        rng = random.Random(seed)

        co_indices = rng.sample(
            range(number_of_atoms),
            number_of_co
        )

        for index in co_indices:
            symbols[index] = "Co"

        atoms.set_chemical_symbols(symbols)

        filename = (
            f"AlCo_{structure_number:02d}"
            f"_Al{actual_al_fraction:.3f}"
            f"_seed{seed}.cif"
        )

        filepath = OUTPUT_FOLDER / filename

        write(filepath, atoms)

        metadata.append([
            structure_number,
            filename,
            number_of_atoms,
            number_of_al,
            number_of_co,
            actual_al_fraction,
            actual_co_fraction,
            seed
        ])

        print(
            f"Created structure {structure_number:02d}: "
            f"Al = {number_of_al}, "
            f"Co = {number_of_co}, "
            f"seed = {seed}"
        )

        structure_number += 1


# --------------------------------------------------
# 5. Save metadata as CSV
# --------------------------------------------------

metadata_file = DATA_FOLDER / "structure_metadata.csv"

with open(metadata_file, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "structure_id",
        "filename",
        "total_atoms",
        "Al_atoms",
        "Co_atoms",
        "Al_fraction",
        "Co_fraction",
        "random_seed"
    ])

    writer.writerows(metadata)


print()
print("---------------------------------------")
print("Structure generation completed.")
print("---------------------------------------")
print("Total structures created:", len(metadata))
print("Structures saved in:", OUTPUT_FOLDER)
print("Metadata saved as:", metadata_file)