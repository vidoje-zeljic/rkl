import sqlite3

import db_util
import excel_reader

con = sqlite3.connect("./rkl.db", check_same_thread=False)
cur = con.cursor()

## query = """
# select *
# from izvestaj
# where (? is null or ? = broj) and (? is null or ? = datum)
# """
# res = cur.execute(query, [None, None, '2023-05-22 20:12:09', '2023-05-22 20:12:09'])
# print(res.fetchall())

def get_resources():
    res = cur.execute("select * from izvestaj;")
    return db_util.db_json_mapper(res)


def save_resources(file_location):
    reports = excel_reader.read_from_excel(file_location)
    cur.executemany("""
    INSERT INTO izvestaj(
        'broj', 
        'datum', 
        'posiljalac', 
        'porucilac', 
        'primalac', 
        'artikal', 
        'prevoznik', 
        'registracija', 
        'vozac', 
        'bruto', 
        'tara', 
        'neto'
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", reports)
    con.commit()


def delete_all():
    cur.execute("delete from izvestaj;")
    con.commit()
