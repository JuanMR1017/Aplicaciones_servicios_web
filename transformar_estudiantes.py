import csv
import json
from pathlib import Path

# Definir las rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent
RUTA_CSV = BASE_DIR / "datos" / "estudiantes.csv"
RUTA_JSON = BASE_DIR / "salida" / "estudiantes_resumen.json"


def transformar_estudiante(fila: dict) -> dict:
    """Transforma un registro individual aplicando las reglas del taller."""
    # Convertir estado 'true'/'false' a 'Activo'/'Inactivo'
    activo_str = str(fila.get("activo", "")).strip().lower()
    es_activo = activo_str in ("true", "1", "verdadero", "yes")
    estado = "Activo" if es_activo else "Inactivo"

    # Concatenar nombre y apellido
    nombre = fila.get("nombre", "").strip()
    apellido = fila.get("apellido", "").strip()
    nombre_completo = f"{nombre} {apellido}".strip()

    return {
        "id": fila.get("codigo"),
        "nombre_completo": nombre_completo,
        "semestre": int(fila.get("semestre", 0)),
        "promedio": float(fila.get("promedio", 0.0)),
        "estado": estado,
    }


def serializar_estudiantes(ruta: Path, estudiantes: list[dict]) -> None:
    """Serializa una lista de diccionarios Python a un archivo JSON UTF-8."""
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(estudiantes, archivo, indent=2, ensure_ascii=False)


def deserializar_estudiantes(ruta: Path) -> list[dict]:
    """Deserializa un archivo JSON a una lista de diccionarios Python."""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


def main():
    print("Hola, Aplicaciones y Servicios Web")

    # Verificar que el CSV exista antes de leerlo
    if not RUTA_CSV.exists():
        print(f"Error: No se encontró el archivo en {RUTA_CSV}")
        return

    # Leer el CSV y transformar cada registro
    estudiantes_transformados = []
    with open(RUTA_CSV, encoding="utf-8") as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        for fila in lector:
            estudiante_modificado = transformar_estudiante(fila)
            estudiantes_transformados.append(estudiante_modificado)

    # Serializar la lista resultante a JSON
    serializar_estudiantes(RUTA_JSON, estudiantes_transformados)
    print(f"Archivo JSON generado: {RUTA_JSON}")

    # Deserializar para comprobar los datos guardados
    estudiantes_recuperados = deserializar_estudiantes(RUTA_JSON)
    print("\nDatos recuperados desde el JSON:")
    if estudiantes_recuperados:
        print(estudiantes_recuperados[0])
    print(f"Total recuperado: {len(estudiantes_recuperados)}")


if __name__ == "__main__":
    main()