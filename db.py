import sqlite3

import db_util

con = sqlite3.connect("./rkl.db", check_same_thread=False)
cur = con.cursor()


def get_resources():
    res = cur.execute("select * from izvestaj;")
    return db_util.db_json_mapper(res)


def save_resources(file_location):
    reports = db_util.reports_file_to_tuple(file_location)
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
