from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. Define folders
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "alco_formation_energy_dataset.csv"
)

FIGURE_FOLDER = (
    PROJECT_ROOT
    / "figures"
)

FIGURE_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


OUTPUT_FIGURE = (
    FIGURE_FOLDER
    / "formation_energy_vs_Al_fraction.png"
)


# --------------------------------------------------
# 2. Read dataset
# --------------------------------------------------

data = pd.read_csv(
    DATA_FILE
)


# --------------------------------------------------
# 3. Calculate mean energy for each composition
# --------------------------------------------------

mean_data = (

    data.groupby(
        "Al_fraction",
        as_index=False
    )

    [
        "formation_energy_eV_per_atom"
    ]

    .mean()
)


# --------------------------------------------------
# 4. Create figure
# --------------------------------------------------

plt.figure(
    figsize=(8, 6)
)


# Individual structures

plt.scatter(
    data["Al_fraction"],
    data["formation_energy_eV_per_atom"],
    s=60,
    label="Individual configurations"
)


# Mean at each composition

plt.plot(
    mean_data["Al_fraction"],
    mean_data["formation_energy_eV_per_atom"],
    marker="o",
    linewidth=2,
    label="Mean at each composition"
)


# Zero-energy reference line

plt.axhline(
    y=0,
    linestyle="--",
    linewidth=1
)


# --------------------------------------------------
# 5. Labels
# --------------------------------------------------

plt.xlabel(
    "Al atomic fraction"
)

plt.ylabel(
    "FCC-constrained formation energy (eV/atom)"
)

plt.title(
    "CHGNet-derived Al-Co formation-energy estimate"
)

plt.legend()

plt.grid(
    alpha=0.3
)

plt.tight_layout()


# --------------------------------------------------
# 6. Save figure
# --------------------------------------------------

plt.savefig(
    OUTPUT_FIGURE,
    dpi=300
)


print()
print(
    "Figure saved as:"
)

print(
    OUTPUT_FIGURE
)


plt.show()