# Guía 2: Limpieza de viajes

## Para qué sirve

Los archivos mensuales de viajes contienen registros que distorsionarían los análisis: viajes de otros meses, estaciones temporales, movimientos del taller, usuarios sin género o edad válidos y errores del sistema. Este proceso aplica las reglas a los nueve meses de una vez y genera un reporte por mes con el resumen de cada regla.

## Qué archivos intervienen

| Tipo | Ruta | Descripción |
|---|---|---|
| Entrada | `data/raw/trips/viajes_ecobici_2026_MM.csv` | Un archivo por mes, enero a septiembre de 2026 |
| Reglas | `scripts/cleaning_rules.json` | Las 11 reglas, en orden. Se editan sin tocar el código |
| Script | `scripts/clean_trips.py` | Procesa todos los archivos de una carpeta |
| Reportes | `data/processed/trips/reports/` | Un reporte JSON por mes y un `summary.csv` |

> **Importante:** el nombre del archivo debe conservar el formato `AAAA_MM`, por ejemplo `viajes_ecobici_2026_09.csv`. El script toma el mes de ahí.

## Pasos para ejecutarlo

1. Abre una terminal dentro de la carpeta `EcoBici`.
2. Ejecuta:

```
python scripts/clean_trips.py data/raw/trips data/processed/trips --solo_reportes
```

3. Revisa la consola: debe aparecer una línea `[OK]` por cada mes.
4. Revisa `data/processed/trips/reports/summary.csv` para el resumen de todos los meses.

El argumento `--solo_reportes` genera solo los reportes. Si lo quitas, el script también escribe un archivo limpio por mes; ocupa unos 700 MB adicionales.

## Cómo leer el reporte

Cada `*_report.json` indica:
- `registros_originales`: viajes del archivo.
- `registros_excluidos` y `registros_conservados`: resultado final.
- `pasos`: cuántos viajes excluyó cada regla, en el orden en que se aplicaron.

Si un mes muestra `"estado": "error: ..."`, ese archivo no se procesó y el mensaje explica la causa.

## Resultado de referencia (enero a septiembre de 2026)

| Concepto | Viajes |
|---|---|
| Originales | 13,877,978 |
| Excluidos | 933,472 (6.73 %) |
| Conservados | 12,944,506 (93.27 %) |

## Cargar en Power BI

Usa la opción de cargar una carpeta y selecciona los archivos de datos limpios. Esta versión genera solo reportes; para cargar datos limpios, ejecuta el script sin `--solo_reportes`.

## Cambiar una regla

Edita `scripts/cleaning_rules.json` y vuelve a ejecutar el script. Consulta la guía 3 para entender cada regla.
