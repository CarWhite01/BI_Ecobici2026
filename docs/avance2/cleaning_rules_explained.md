# Guía 3: Reglas de limpieza

Las reglas se aplican en el orden indicado. Cada regla cuenta solo los viajes que no fueron excluidos por una regla anterior, por eso el orden importa. Las cifras son del total anual (enero a septiembre de 2026).

| # | Regla | Motivo | Excluidos (ene–sep) |
|---|---|---|---|
| 1 | Arribo fuera del mes del archivo | El mes del viaje lo define la fecha de arribo, porque la fuente se corta por esa fecha. En los nueve archivos no hay arribos fuera de su mes | 0 |
| 2 | Estación temporal (`Temporal N`) | Infraestructura transitoria de abril a julio de 2026, habilitada para conectar la red de movilidad integrada con puntos de afluencia turística durante la Copa Mundial FIFA 2026. No forma parte del catálogo permanente y su ubicación no es estable | 1,326 |
| 3 | Estación de taller (código `1000`) | Las bicicletas que entran o salen del taller de mantenimiento no corresponden a un viaje de usuario | 407 |
| 4 | Edad faltante | Sin edad no se puede clasificar al usuario por rango | 440 |
| 5 | Género desconocido (`?`) | Sin género no se puede ubicar en los análisis por género | 420,850 |
| 6 | Menores de 18 años | No corresponden al perfil de usuario esperado | 6,668 |
| 7 | Mayores de 99 años | Control para errores de captura | 28 |
| 8 | Origen igual a destino | No representa un desplazamiento real y distorsiona las rutas | 367,439 |
| 9 | Duración menor a 1 minuto | Suelen ser retiros fallidos o errores del sistema | 1,636 |
| 10 | Duración mayor a 45 min, lunes a jueves | Criterio del equipo, pendiente de validar con el área operativa | 94,298 |
| 11 | Duración mayor a 60 min, viernes a domingo | Criterio del equipo, pendiente de validar con el área operativa | 40,380 |

## Cómo cambiar una regla

Abre `scripts/cleaning_rules.json`. Cada regla tiene un `id`, un operador y, según el caso, un campo, un valor o un patrón. Por ejemplo, para cambiar el mínimo de edad de 18 a 16:

```json
{"id": "minor_users", "field": "edad", "operator": "lt", "value": 16, "description": "..."}
```

Operadores disponibles:
- `lt` (menor que), `gt` (mayor que), `eq` (igual a) y `is_null` (vacío), sobre `genero`, `edad` o `duracion_min`.
- `outside_period` (fuera del mes del archivo, por fecha de arribo).
- `station_pattern` (patrón en cualquiera de las dos estaciones, por ejemplo `^Temporal \d+$`).
- `station_equals` (código exacto en cualquiera de las dos estaciones).
- `same_station` (origen igual a destino).
