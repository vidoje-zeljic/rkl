import openpyxl


def read_from_excel(file_location, file_id):
    sh = openpyxl.load_workbook(file_location).active
    reports = []
    for row in range(1, sh.max_row+1):
        if sh.cell(row=row, column=2).value is not None:
            report = (
                int(sh.cell(row=row, column=3).value),
                str(sh.cell(row=row, column=4).value),
                sh.cell(row=row, column=5).value,
                sh.cell(row=row, column=6).value,
                sh.cell(row=row, column=7).value,
                sh.cell(row=row, column=8).value,
                sh.cell(row=row, column=9).value,
                sh.cell(row=row, column=10).value,
                sh.cell(row=row, column=11).value,
                float(sh.cell(row=row, column=12).value),
                float(sh.cell(row=row, column=13).value),
                float(sh.cell(row=row, column=14).value),
                file_id
            )
            reports.append(report)
    return reports
