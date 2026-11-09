# Guía 1: Filtrado de cicloestaciones

## Para qué sirve
Reduce el catálogo completo de estaciones de Ecobici a solo cuatro datos por estación:
identificador, nombre, latitud y longitud. Sirve para ubicar las estaciones en un mapa
o para unirlas con los viajes en Power BI.

## Qué archivos intervienen

| Tipo | Ruta | Descripción |
|---|---|---|
| Entrada | `data/raw/stations/station_information.json` | Catálogo original de la API (677 estaciones) |
| Script | `scripts/filter_bike_stations.py` | Hace el filtrado |
| Salida | `data/processed/stations/filtered_stations.json` | Estaciones con los cuatro datos |

## Pasos para ejecutarlo

1. Abre una terminal dentro de la carpeta `EcoBici`.
2. Ejecuta el comando:

```
python scripts/filter_bike_stations.py data/raw/stations/station_information.json data/processed/stations/filtered_stations.json
```

3. Verifica el mensaje final: `Se crearon 677 estaciones en: ...`.

**Prueba con pocas estaciones:** agrega un número al final para procesar solo las primeras N.

```
python scripts/filter_bike_stations.py data/raw/stations/station_information.json prueba.json 5
```

## Ejemplo de salida

```json
{
  "station_id": "1",
  "nombre": "CE-710 Molino del Rey - Glorieta de la Lealtad",
  "lat": 19.416795,
  "lon": -99.192508
}
```

## Errores comunes
- `FileNotFoundError`: no estás en la carpeta `EcoBici`, o la ruta del JSON está mal escrita.
- `python` no se reconoce: usa la ruta completa de tu Python o activa tu entorno de Anaconda.
