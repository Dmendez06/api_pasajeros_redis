import json
from datetime import datetime
from pathlib import Path

DATOS = Path(__file__).resolve().parent.parent / "datos"

CLAVES = {
    "Código Ruta": "codigo_ruta",
    "Nombre Ruta": "nombre_ruta",
    "Nombre Fraccionamiento": "nombre_fraccionamiento",
    "Km por Viaje (Promedio)": "km_por_viaje",
    "Tarifa Regular (¢)": "tarifa_regular",
    "Tarifa Adulto Mayor (¢)": "tarifa_adulto_mayor",
    "Resolución": "resolucion",
    "Fecha Resolución": "fecha_resolucion",
    "Gaceta": "gaceta",
    "Alcance": "alcance",
    "Fecha Gaceta": "fecha_gaceta",
    "Fecha Vigencia": "fecha_vigencia",
    "Expediente": "expediente",
    "Operadores": "operadores",
    "Cédulas": "cedulas",
}
DECIMALES = {"km_por_viaje", "tarifa_regular", "tarifa_adulto_mayor"}
ENTEROS = {"gaceta", "alcance"}
FECHAS = {"fecha_resolucion", "fecha_gaceta", "fecha_vigencia"}


def normalizar(doc: dict) -> dict:
    out = {}
    for clave, valor in doc.items():
        nueva = CLAVES[clave]
        if nueva in DECIMALES:
            valor = float(valor)
        elif nueva in ENTEROS:
            valor = int(valor)
        elif nueva in FECHAS:
            valor = {"$date": datetime.strptime(valor, "%d-%m-%Y").strftime("%Y-%m-%dT00:00:00Z")}
        out[nueva] = valor
    return out


if __name__ == "__main__":
    original = json.loads((DATOS / "tarifas_original.json").read_text(encoding="utf-8"))
    nuevo = [normalizar(d) for d in original]
    (DATOS / "tarifas.json").write_text(json.dumps(nuevo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(nuevo)} tarifas escritas en datos/tarifas.json")
