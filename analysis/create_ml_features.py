from pathlib import Path

import pandas as pd

from ase.io import read
from ase.neighborlist import neighbor_list


# --------------------------------------------------
# 1. Define folders
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

STRUCTURE_FOLDER = (
    PROJECT_ROOT
    / "structures"
    / "generated"
)

FORMATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "alco_formation_energy_dataset.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "ml_feature_dataset.csv"
)


# --------------------------------------------------
# 2. Read formation-energy dataset
# --------------------------------------------------

formation_data = pd.read_csv(
    FORMATION_FILE
)


# --------------------------------------------------
# 3. First-neighbor cutoff
# --------------------------------------------------

# For FCC with a = 4.05 Angstrom,
# nearest-neighbor distance is about 2.86 Angstrom.
#
# 3.10 Angstrom therefore captures approximately
# the first coordination shell.

cutoff = 3.10


# --------------------------------------------------
# 4. Storage
# --------------------------------------------------

feature_rows = []


# --------------------------------------------------
# 5. Process each structure
# --------------------------------------------------

for _, row in formation_data.iterrows():

    filename = row["filename"]

    structure_file = (
        STRUCTURE_FOLDER
        / filename
    )

    atoms = read(
        structure_file
    )

    symbols = atoms.get_chemical_symbols()


    # Obtain neighbor atom indices

    i_list, j_list = neighbor_list(
        "ij",
        atoms,
        cutoff
    )


    al_al_pairs = 0
    al_co_pairs = 0
    co_co_pairs = 0


    # neighbor_list usually contains both directions,
    # so count only i < j.

    for i, j in zip(
        i_list,
        j_list
    ):

        if i >= j:
            continue


        pair = {
            symbols[i],
            symbols[j]
        }


        if (
            symbols[i] == "Al"
            and symbols[j] == "Al"
        ):

            al_al_pairs += 1


        elif (
            symbols[i] == "Co"
            and symbols[j] == "Co"
        ):

            co_co_pairs += 1


        else:

            al_co_pairs += 1


    total_pairs = (
        al_al_pairs
        + al_co_pairs
        + co_co_pairs
    )


    # Convert counts to fractions

    al_al_fraction = (
        al_al_pairs
        / total_pairs
    )

    al_co_fraction = (
        al_co_pairs
        / total_pairs
    )

    co_co_fraction = (
        co_co_pairs
        / total_pairs
    )


    feature_rows.append({

        "structure_id":
            row["structure_id"],

        "filename":
            filename,

        "Al_fraction":
            row["Al_fraction"],

        "Al_Al_pair_fraction":
            al_al_fraction,

        "Al_Co_pair_fraction":
            al_co_fraction,

        "Co_Co_pair_fraction":
            co_co_fraction,

        "formation_energy_eV_per_atom":
            row[
                "formation_energy_eV_per_atom"
            ]

    })


# --------------------------------------------------
# 6. Save feature dataset
# --------------------------------------------------

feature_data = pd.DataFrame(
    feature_rows
)


feature_data.to_csv(
    OUTPUT_FILE,
    index=False
)


print()
print("----------------------------------------")
print("ML FEATURE DATASET CREATED")
print("----------------------------------------")

print(
    feature_data.to_string(
        index=False
    )
)

print()
print(
    "Saved as:"
)

print(
    OUTPUT_FILE
)

print("----------------------------------------")