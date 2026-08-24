from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. Define folders
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FOLDER = (
    PROJECT_ROOT
    / "data"
)


ALLOY_FILE = (
    DATA_FOLDER
    / "chgnet_energy_dataset.csv"
)

REFERENCE_FILE = (
    DATA_FOLDER
    / "chgnet_reference_energies.csv"
)


OUTPUT_FILE = (
    DATA_FOLDER
    / "alco_formation_energy_dataset.csv"
)


# --------------------------------------------------
# 2. Read datasets
# --------------------------------------------------

alloy_data = pd.read_csv(
    ALLOY_FILE
)

reference_data = pd.read_csv(
    REFERENCE_FILE
)


# --------------------------------------------------
# 3. Extract Al and Co reference energies
# --------------------------------------------------

al_reference_energy = float(

    reference_data.loc[
        reference_data["element"] == "Al",
        "energy_eV_per_atom"
    ].iloc[0]

)


co_reference_energy = float(

    reference_data.loc[
        reference_data["element"] == "Co",
        "energy_eV_per_atom"
    ].iloc[0]

)


print()
print("----------------------------------------")
print("REFERENCE ENERGIES")
print("----------------------------------------")

print(
    "Al FCC reference:",
    al_reference_energy,
    "eV/atom"
)

print(
    "Co FCC reference:",
    co_reference_energy,
    "eV/atom"
)


# --------------------------------------------------
# 4. Calculate formation-energy estimate
# --------------------------------------------------

alloy_data[
    "reference_energy_eV_per_atom"
] = (

    alloy_data["Al_fraction"]
    * al_reference_energy

    +

    alloy_data["Co_fraction"]
    * co_reference_energy
)


alloy_data[
    "formation_energy_eV_per_atom"
] = (

    alloy_data[
        "CHGNet_energy_eV_per_atom"
    ]

    -

    alloy_data[
        "reference_energy_eV_per_atom"
    ]
)


# --------------------------------------------------
# 5. Save result
# --------------------------------------------------

alloy_data.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# 6. Print important columns
# --------------------------------------------------

print()
print("----------------------------------------")
print("FORMATION ENERGY RESULTS")
print("----------------------------------------")

print(
    alloy_data[
        [
            "structure_id",
            "Al_fraction",
            "Co_fraction",
            "CHGNet_energy_eV_per_atom",
            "formation_energy_eV_per_atom"
        ]
    ].to_string(
        index=False
    )
)


print()
print("----------------------------------------")

print(
    "Saved as:"
)

print(
    OUTPUT_FILE
)

print("----------------------------------------")