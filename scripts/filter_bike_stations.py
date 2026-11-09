import json
import sys

def filtrar_estaciones(ruta, limite=None):
    """Devuelve identificador, nombre, latitud y longitud de cada estación.
    Si se indica 'limite', solo procesa las primeras N estaciones."""
    with open(ruta, encoding="utf-8") as f:
        estaciones = json.load(f)["data"]["stations"]

    if limite is not None:
        estaciones = estaciones[:limite]

    return [
        {
            "station_id": e["station_id"],
            "nombre": e["name"],
            "lat": e["lat"],
            "lon": e["lon"],
        }
        for e in estaciones
    ]

if __name__ == "__main__":
    ruta_entrada = sys.argv[1] if len(sys.argv) > 1 else "station_information.json"
    ruta_salida = sys.argv[2] if len(sys.argv) > 2 else "filtered_stations.json"
    limite = int(sys.argv[3]) if len(sys.argv) > 3 else None

    resultado = filtrar_estaciones(ruta_entrada, limite)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"Se crearon {len(resultado)} estaciones en: {ruta_salida}")
