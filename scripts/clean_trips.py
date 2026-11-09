"""Limpia los archivos mensuales de viajes Ecobici de una carpeta.

Uso:
    python clean_trips.py <carpeta_entrada> <carpeta_salida> [--rules cleaning_rules.json] [--solo_reportes]

Con --solo_reportes solo se generan los reportes (no los archivos limpios).
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

import pandas as pd

EXPECTED_COLUMNS = [
    "Genero_Usuario", "Edad_Usuario", "Bici", "Ciclo_Estacion_Retiro",
    "Fecha_Retiro", "Hora_Retiro", "Ciclo_EstacionArribo", "Fecha_Arribo", "Hora_Arribo",
]
DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
FIELD_MAP = {"genero": "Genero_Usuario", "edad": "_edad", "duracion_min": "_duracion_min"}
STATION_COLUMNS = ["Ciclo_Estacion_Retiro", "Ciclo_EstacionArribo"]


def load_rules(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["rules"]


def load_and_validate(path):
    df = pd.read_csv(path, dtype=str)
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas: {missing}")

    retiro = pd.to_datetime(df["Fecha_Retiro"] + " " + df["Hora_Retiro"], format=DATE_FORMAT, errors="coerce")
    arribo = pd.to_datetime(df["Fecha_Arribo"] + " " + df["Hora_Arribo"], format=DATE_FORMAT, errors="coerce")
    invalid = int(retiro.isna().sum() + arribo.isna().sum())
    if invalid:
        raise ValueError(f"{invalid} fechas u horas no válidas")

    df["_retiro"] = retiro
    df["_arribo"] = arribo
    df["_duracion_min"] = (arribo - retiro).dt.total_seconds() / 60
    df["_dia_semana"] = retiro.dt.dayofweek  # 0 = lunes ... 6 = domingo
    df["_edad"] = pd.to_numeric(df["Edad_Usuario"], errors="coerce")
    return df


def period_from_filename(name):
    match = re.search(r"(\d{4})_(\d{2})", name)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def station_either(df, condition):
    """True si la condición se cumple en la estación de retiro o en la de arribo."""
    return condition(df[STATION_COLUMNS[0]].fillna("")) | condition(df[STATION_COLUMNS[1]].fillna(""))


def apply_rule(df, rule, period):
    op = rule["operator"]
    if op == "outside_period":
        if period is None:
            raise ValueError("No se encontró el periodo (AAAA_MM) en el nombre del archivo")
        year, month = period
        # El mes del viaje lo define la fecha de arribo
        return (df["_arribo"].dt.year != year) | (df["_arribo"].dt.month != month)
    if op == "same_station":
        return df["Ciclo_Estacion_Retiro"] == df["Ciclo_EstacionArribo"]
    if op == "station_pattern":
        pattern = rule["pattern"]
        return station_either(df, lambda s: s.str.match(pattern))
    if op == "station_equals":
        value = rule["value"]
        return station_either(df, lambda s: s == value)

    series = df[FIELD_MAP[rule["field"]]]
    if op == "is_null":
        mask = series.isna()
    elif op == "eq":
        mask = series == rule["value"]
    elif op == "lt":
        mask = series < rule["value"]
    elif op == "gt":
        mask = series > rule["value"]
    else:
        raise ValueError(f"Operador no soportado: {op}")

    if "days" in rule:
        mask = mask & df["_dia_semana"].isin(rule["days"])
    return mask.fillna(False).astype(bool)


def clean_file(path, rules, output_dir, solo_reportes=False):
    df = load_and_validate(path)
    period = period_from_filename(path.stem)
    total = len(df)

    remaining = pd.Series(True, index=df.index)
    steps = []
    for rule in rules:
        mask = apply_rule(df, rule, period)
        excluded = int((mask & remaining).sum())
        remaining &= ~mask
        steps.append({"regla": rule["id"], "descripcion": rule["description"], "excluidos": excluded})

    kept = int(remaining.sum())
    out_name = None
    if not solo_reportes:
        out_csv = output_dir / f"{path.stem}_clean.csv"
        df.loc[remaining, EXPECTED_COLUMNS].to_csv(out_csv, index=False, encoding="utf-8")
        out_name = out_csv.name

    return {
        "archivo": path.name,
        "estado": "ok",
        "periodo": f"{period[0]}-{period[1]:02d}" if period else None,
        "registros_originales": total,
        "registros_excluidos": total - kept,
        "registros_conservados": kept,
        "porcentaje_conservado": round(kept / total * 100, 2) if total else 0,
        "pasos": steps,
        "salida": out_name,
    }


def main():
    parser = argparse.ArgumentParser(description="Limpieza de viajes Ecobici por lotes")
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--rules", default=str(Path(__file__).with_name("cleaning_rules.json")))
    parser.add_argument("--solo_reportes", action="store_true", help="Genera solo reportes, sin archivos limpios")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    reports_dir = output_dir / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(input_dir.glob("*.csv"))
    if not files:
        print(f"No se encontraron archivos .csv en {input_dir}")
        sys.exit(1)

    rules = load_rules(args.rules)
    summary = []

    for path in files:
        try:
            report = clean_file(path, rules, output_dir, solo_reportes=args.solo_reportes)
        except Exception as e:
            report = {"archivo": path.name, "estado": f"error: {e}"}
            print(f"[ERROR] {path.name}: {e}")
        else:
            print(f"[OK] {path.name}: {report['registros_conservados']:,} de {report['registros_originales']:,} conservados")

        with open(reports_dir / f"{path.stem}_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        summary.append({
            "archivo": report["archivo"],
            "estado": report["estado"],
            "originales": report.get("registros_originales", ""),
            "excluidos": report.get("registros_excluidos", ""),
            "conservados": report.get("registros_conservados", ""),
            "porcentaje_conservado": report.get("porcentaje_conservado", ""),
        })

    with open(reports_dir / "summary.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)
    print(f"Reportes en: {reports_dir}")


if __name__ == "__main__":
    main()
