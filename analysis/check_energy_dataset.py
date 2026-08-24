from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "chgnet_energy_dataset.csv"
)


data = pd.read_csv(
    DATA_FILE
)


print()
print("----------------------------------------")
print("ENERGY DATASET CHECK")
print("----------------------------------------")

print(
    "Number of rows:",
    len(data)
)

print()


print("Column names:")

for column in data.columns:

    print("-", column)


print()
print("First five rows:")
print()

print(
    data.head()
)


print()
print("Energy statistics:")
print()

print(
    data[
        "CHGNet_energy_eV_per_atom"
    ].describe()
)


print()
print("----------------------------------------")