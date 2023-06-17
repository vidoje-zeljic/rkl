def format_date(date):
    tmp = date.split("-")
    return tmp[2] + "-" + tmp[1] + "-" + tmp[0]


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
