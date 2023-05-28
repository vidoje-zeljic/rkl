import pyfiglet
import os
import util
import json
import sqlite3

print(pyfiglet.figlet_format("RKL"))

reports = []

csv_dir = os.fsencode("resources/csv")

for csv_file in os.listdir(csv_dir):
    reports.extend(util.read_reports_from_csv(f"resources/csv/{os.fsdecode(csv_file)}"))


# print(json.dumps(r, indent=4))
reports = util.prepare_for_insert(reports)

con = sqlite3.connect("resources/db/tutorial.db")
cur = con.cursor()

# res = cur.execute("select * from izvestaj;")
# print(res.fetchall())

cur.executemany("""
    INSERT INTO izvestaj ('broj', 'datum', 'posiljalac', 'porucilac', 'primalac', 'artikal', 'prevoznik', 'registracija', 'vozac', 'bruto', 'tara', 'neto')
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", reports)

con.commit()
