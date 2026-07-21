# ============================================================
# verify_dataset.py
#
# Verifica que el dataset de referencia corresponde a la firma
# almacenada en dataset_signature.json
#
# FFTN_BTC_1D
# ============================================================

import hashlib
import json
from pathlib import Path


# ------------------------------------------------------------
# Rutas
# ------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

SIGNATURE_FILE = ROOT / "reference" / "baseline" / "dataset_signature.json"


# ------------------------------------------------------------
# Leer firma
# ------------------------------------------------------------

with open(SIGNATURE_FILE, "r", encoding="utf-8") as f:
    signature = json.load(f)

dataset_path = ROOT / Path(signature["location"])

expected_hash = signature["sha256"]


# ------------------------------------------------------------
# Calcular SHA256
# ------------------------------------------------------------

sha256 = hashlib.sha256()

with open(dataset_path, "rb") as f:
    for chunk in iter(lambda: f.read(8192), b""):
        sha256.update(chunk)

current_hash = sha256.hexdigest()


# ------------------------------------------------------------
# Mostrar información
# ------------------------------------------------------------

print()
print("=" * 50)
print("DATASET VERIFICATION")
print("=" * 50)

print(f"Dataset : {signature['dataset']}")
print(f"Location: {dataset_path}")
print(f"Rows    : {signature['rows']}")
print(f"Columns : {len(signature['columns'])}")
print()

print("Expected SHA256:")
print(expected_hash)
print()

print("Current SHA256:")
print(current_hash)
print()


# ------------------------------------------------------------
# Resultado
# ------------------------------------------------------------

if current_hash == expected_hash:
    print("✔ Dataset verified successfully.")
else:
    print("✘ Dataset verification FAILED.")
    raise SystemExit(1)