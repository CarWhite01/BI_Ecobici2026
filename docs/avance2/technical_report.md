# Reporte técnico: preparación de datos de viajes y estaciones de Ecobici CDMX 2026

**Proyecto:** Patrones de uso y comportamiento territorial de Ecobici CDMX
**Equipo:** LOS CAMPECHANOS · Inteligencia de Negocios, semestre 2026-2 · UACM

| Integrante | Responsabilidad |
|---|---|
| Carlos Josafat Fragoso Palma | Libreta de Jupyter |
| Edson Joel Carrera Ávila | Obtención y limpieza de datos |
| Francisco Javier García Rojas | Documentación |

---

## 1. Resumen

- Se revisaron **13,877,978 viajes** de enero a septiembre de 2026, nueve archivos mensuales. Octubre a diciembre aún no están publicados.
- Se aplicaron **11 reglas** de limpieza, en orden. Se excluyeron **933,472 viajes (6.73 %)**. Se conservan **12,944,506 (93.27 %)**.
- En cada mes se conserva entre el 92.98 % y el 93.68 % de los viajes, con el mismo proceso.
- El catálogo de estaciones corresponde a noviembre de 2026 e incluye las estaciones que se abrieron y retiraron durante el año. Los viajes usan estaciones del catálogo en todos los meses, salvo los códigos especiales (`1000` y `Temporal N`), que se excluyen por regla.
- Los resultados sirven para analizar uso por estación, horario y ruta. Antes de usar el perfil por género o edad, hay que resolver los pendientes de la sección 8.

## 2. Pregunta que guía el análisis

¿Cómo varía el uso de Ecobici entre estaciones y zonas durante 2026, y qué características tienen los lugares con mayor y menor uso?

**Quién lo usaría:** Dirección de Movilidad Sostenible de SEMOVI y urbanistas, como apoyo para decisiones de operación e infraestructura.

## 3. Fuentes de datos

| Fuente | Contenido | Tamaño | Ubicación |
|---|---|---|---|
| Viajes mensuales, enero a septiembre de 2026 (API oficial, portal de datos abiertos de la CDMX) | Un registro por viaje: estaciones de retiro y arribo, fechas, horas, bicicleta, género y edad | 13,877,978 filas en total, 9 columnas | `data/raw/trips/` |
| Catálogo de estaciones (feed GBFS, API oficial) | Código, nombre, latitud, longitud y capacidad de cada estación. Fecha de corte: 8 de noviembre de 2026 | 677 estaciones | `data/raw/stations/station_information.json` |

**Pendiente:** la fecha de descarga de los viajes no quedó registrada. Debe anotarse en el contrato de lectura.

## 4. Proceso

El trabajo se hizo en cuatro etapas. Cada una tiene su archivo, de modo que cualquier integrante puede repetirla.

**Etapa A. Catálogo de estaciones.** `scripts/filter_bike_stations.py` reduce el catálogo a identificador, nombre, latitud y longitud.

**Etapa B. Lectura, perfil y comprobaciones.** La libreta `notebooks/avance2_ecobici.ipynb` lee los viajes y revisa cada mes con el mismo perfil: columnas, duplicados, arribos fuera del mes, cobertura del catálogo y un extracto de 10 filas.

**Etapa C. Filtro de análisis.** Las reglas están en `scripts/cleaning_rules.json`. Se aplican en orden y cada una cuenta solo los viajes que no excluyó una anterior. La libreta usa las mismas funciones que el script, así que ambos dan el mismo resultado.

**Etapa D. Procesamiento por lotes.** `scripts/clean_trips.py` aplica las reglas a todos los meses de una carpeta y genera un reporte por mes y un resumen. Con `--solo_reportes` no escribe archivos limpios.

## 5. Reglas de limpieza

Las reglas se aplican en orden. Las cifras son del total de enero a septiembre.

| # | Regla | Motivo | Excluidos |
|---|---|---|---|
| 1 | Arribo fuera del mes del archivo | El mes lo define la fecha de arribo, porque la fuente se corta por esa fecha | 0 |
| 2 | Estación temporal (`Temporal N`) | Infraestructura transitoria de abril a julio de 2026, para conectar la red con puntos de afluencia turística durante la Copa Mundial FIFA 2026. No forma parte del catálogo permanente | 1,326 |
| 3 | Estación de taller (`1000`) | Movimientos de bicicletas hacia o desde el taller de mantenimiento, no viajes de usuario | 407 |
| 4 | Edad faltante | Sin edad no se puede clasificar al usuario | 440 |
| 5 | Género desconocido (`?`) | Sin género no se puede ubicar en análisis por género | 420,850 |
| 6 | Menores de 18 años | No corresponden al perfil de usuario esperado | 6,668 |
| 7 | Mayores de 99 años | Control para errores de captura | 28 |
| 8 | Origen igual a destino | No representa un desplazamiento real | 367,439 |
| 9 | Duración menor a 1 minuto | Suelen ser retiros fallidos o errores del sistema | 1,636 |
| 10 | Duración mayor a 45 min, lunes a jueves | Criterio del equipo, pendiente de validar | 94,298 |
| 11 | Duración mayor a 60 min, viernes a domingo | Criterio del equipo, pendiente de validar | 40,380 |

**Por qué el mes lo define el arribo.** Un viaje que sale el 31 de agosto y llega el 1 de septiembre cuenta en septiembre. Con la fecha de retiro se perderían esos viajes. En los nueve archivos no hay arribos fuera de su mes.

**Nota sobre las reglas 10 y 11.** Los umbrales los definió el equipo. No provienen de una norma ni de la documentación de la fuente. Deben validarse con el área operativa antes de presentarlos como criterio oficial.

**Nota sobre la regla 7.** Hay registros de 97 y 98 años, que se conservan porque la regla excluye solo a partir de 100 años. La regla de 99 años excluye 28 viajes en el año.

## 6. Resultados por mes

| Mes | Originales | Excluidos | Conservados | % conservado |
|---|---|---|---|---|
| Enero | 1,525,302 | 103,490 | 1,421,812 | 93.22 |
| Febrero | 1,528,610 | 106,978 | 1,421,632 | 93.00 |
| Marzo | 1,653,373 | 116,042 | 1,537,331 | 92.98 |
| Abril | 1,594,967 | 109,562 | 1,485,405 | 93.13 |
| Mayo | 1,615,360 | 108,324 | 1,507,036 | 93.29 |
| Junio | 1,494,265 | 102,428 | 1,391,837 | 93.15 |
| Julio | 1,493,484 | 96,489 | 1,396,995 | 93.54 |
| Agosto | 1,473,683 | 95,480 | 1,378,203 | 93.52 |
| Septiembre | 1,498,934 | 94,679 | 1,404,255 | 93.68 |
| **Total** | **13,877,978** | **933,472** | **12,944,506** | **93.27** |

**Comprobaciones de los nueve meses:** columnas esperadas, cero duplicados exactos, cero arribos fuera del mes y conservados más excluidos iguales a originales. Todas cumplen.

**Cambio respecto a la versión anterior de septiembre.** Con la regla de arribo, septiembre conserva 1,404,255 viajes (antes 1,404,180), porque se recuperan los viajes que salieron en agosto y llegaron en septiembre. Las reglas nuevas excluyen 1,326 viajes temporales y 407 del taller en todo el año.

## 7. Ajustes respecto al avance 1

| Tema | Avance 1 | Avance 2 | Motivo |
|---|---|---|---|
| Fuente principal | Kaggle. El portal oficial quedaba como respaldo | API oficial, portal de datos abiertos de la CDMX | Procedencia verificable y datos de 2026. Kaggle podía tener desfase de meses |
| Variables de viajes | Sin estación de retiro ni de arribo | 9 columnas, con estaciones | Sin estaciones no se puede responder la pregunta por estación |
| Alcance | Más de 80 millones de viajes (2010 a la fecha) | Enero a septiembre de 2026, 13.9 millones de viajes | Periodo disponible por publicación de la CDMX |
| Catálogo de estaciones | No contemplado | Catálogo de la API oficial (677 estaciones) | El archivo de viajes solo trae códigos |
| Regla de edad | Filtrar mayores de 100 | Excluir mayores de 99 | Regla del equipo. El máximo observado es 98 |
| Periodo | No definido | Mes por fecha de arribo | La fuente se corta por esa fecha |

## 8. Glosario

| Término | Significado |
|---|---|
| GBFS | Formato abierto que usan los sistemas de bicicletas compartidas para publicar sus estaciones y su estado |
| `short_name` | Código corto de la estación (por ejemplo `022`). Es el que aparece en los viajes |
| Código `1000` | Taller de mantenimiento. Sus movimientos no son viajes de usuario |
| Estación temporal | Estación `Temporal N`, instalada de forma transitoria de abril a julio de 2026 |
| Fecha de arribo | Momento en que la bicicleta llega a la estación de destino. Define el mes del viaje |
| Regla acumulada | Cada regla cuenta solo los viajes que no excluyó una regla anterior |
| Filtro de análisis | Exclusión de viajes según las reglas del proyecto. No corrige datos: solo decide qué entra al análisis |
