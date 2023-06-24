def format_date(date):
    tmp = date.split("-")
    return tmp[2] + "-" + tmp[1] + "-" + tmp[0]


def db_json_mapper(tuple_reports):
    json_reports = []
    for json_report in tuple_reports:
        report = {
            "broj": json_report[1],
            "datum": json_report[2],
            "vreme": json_report[3],
            "posiljalac": json_report[4],
            "porucilac": json_report[5],
            "primalac": json_report[6],
            "artikal": json_report[7],
            "prevoznik": json_report[8],
            "registracija": json_report[9],
            "vozac": json_report[10],
            "bruto": format_number(json_report[11]),
            "tara": format_number(json_report[12]),
            "neto": format_number(json_report[13]),
            "mesto": (json_report[14] if json_report[14] else ""),
        }
        json_reports.append(report)
    return json_reports


def format_number(number):
    return f'{int(number):,}'
