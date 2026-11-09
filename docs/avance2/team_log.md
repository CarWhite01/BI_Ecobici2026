# Bitácora del equipo · LOS CAMPECHANOS

**Proyecto:** Patrones de uso y comportamiento territorial de Ecobici CDMX
**Asignaturas:** Inteligencia de Negocios, semestre 2026-2 · UACM
**Corte de la bitácora:** avance 2

| Tarea | Responsable | Evidencia | Estado |
|---|---|---|---|
| Creación de la libreta de Jupyter por mes: ejecución de scripts, revisión de nueve meses, validación y conclusiones | Carlos Josafat Fragoso Palma | `notebooks/avance2_ecobici.ipynb` (ejecutada sin errores), `data/processed/avance2/resumen_meses.csv` | Completada |
| Obtención de los viajes de septiembre 2026 desde el portal de datos abiertos de la CDMX (API oficial) | Edson Joel Carrera Ávila | `data/raw/trips/viajes_ecobici_2026_09.csv` | Completada. Falta registrar la fecha de descarga |
| Obtención del catálogo de estaciones (API oficial) | Edson Joel Carrera Ávila | `data/raw/stations/station_information.json` | Completada |
| Limpieza de datos: reglas de exclusión y procesamiento por lotes (11 reglas, enero a septiembre) | Edson Joel Carrera Ávila | `scripts/clean_trips.py`, `scripts/cleaning_rules.json`, `data/processed/trips/reports/` | Completada |
| Filtrado del catálogo de estaciones | Edson Joel Carrera Ávila (asignación por confirmar) | `scripts/filter_bike_stations.py`, `data/processed/stations/filtered_stations.json` | Completada. Confirmar responsable |
| Documentación: readme, guías de uso, reglas y reporte técnico | Francisco Javier García Rojas | `readme.md`, `docs/` | En revisión |
| Bitácora del equipo | Francisco Javier García Rojas | `docs/team_log.md` | En revisión |
| Retroalimentación del avance 1: observación, acción y evidencia | Sin responsable asignado | Pendiente: la observación no está en los archivos de esta etapa | Pendiente |
| Presentación del avance 2 y demostración en vivo | Sin responsable asignado | Pendiente: carpeta `presentacion/` no creada | Pendiente |
| Verificación de ejecución desde el inicio en un equipo distinto del de desarrollo | Sin responsable asignado | Pendiente | Pendiente |

| Definición de reglas nuevas: estaciones temporales, taller (código 1000) y periodo por arribo | Edson Joel Carrera Ávila (confirmar) | `scripts/cleaning_rules.json`, guía 3 | Completada. Pendiente cita de la fuente de estaciones temporales |
