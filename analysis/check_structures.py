from pathlib import Path
from ase.io import read


PROJECT_ROOT = Path(__file__).resolve().parents[1]

STRUCTURE_FOLDER = PROJECT_ROOT / "structures" / "generated"

files = sorted(STRUCTURE_FOLDER.glob("*.cif"))


print("Number of CIF files found:", len(files))
print()


for file in files:

    atoms = read(file)

    symbols = atoms.get_chemical_symbols()

    number_of_al = symbols.count("Al")
    number_of_co = symbols.count("Co")

    print(
        file.name,
        "| Total atoms:",
        len(atoms),
        "| Al:",
        number_of_al,
        "| Co:",
        number_of_co
    )