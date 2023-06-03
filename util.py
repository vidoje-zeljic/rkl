def format_date(date):
    tmp = date.split(".")
    return tmp[2] + "-" + tmp[1] + "-" + tmp[0]


def read_reports_from_csv(file):
    reports_file = open(file, "r").read().split("\n")

    reports = []
    for line in reports_file:
        if not line.startswith(";") and not line.startswith("﻿;"):
            report_columns = line.split(";")
            report = {
                "broj": int(report_columns[1]),
                "datum": format_date(report_columns[2]),
                "posiljalac": report_columns[3],
                "porucilac": report_columns[4],
                "primalac": report_columns[5],
                "artikal": report_columns[6],
                "prevoznik": report_columns[7],
                "registracija": report_columns[8],
                "vozac": report_columns[9],
                "bruto": float(report_columns[10]),
                "tara": float(report_columns[11]),
                "neto": float(report_columns[12]),
            }
            reports.append(report)
    return reports


def db_json_mapper(tuple_reports):
    json_reports = []
    for json_report in tuple_reports:
        report = {
            "broj": json_report[1],
            "datum": json_report[2],
            "posiljalac": json_report[3],
            "porucilac": json_report[4],
            "primalac": json_report[5],
            "artikal": json_report[6],
            "prevoznik": json_report[7],
            "registracija": json_report[8],
            "vozac": json_report[9],
            "bruto": json_report[10],
            "tara": json_report[11],
            "neto": json_report[12],
        }
        json_reports.append(report)
    return json_reports


def prepare_for_insert(reports):
    reports_tuples = []
    for r in reports:
        reports_tuples.append(tuple(r.values()))
    return reports_tuples
