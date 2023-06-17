import sqlite3

import db_util
import excel_reader
from datetime import datetime

DT_FORMAT = "%Y-%m-%d %H:%M:%S"

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


def get_files():
    return cur.execute("select * from file;").fetchall()


def save_file(file_name):
    result = cur.execute("""
    INSERT INTO file(name, upload_dt)
    VALUES(?, ?)""", [file_name, datetime.now().strftime(DT_FORMAT)])
    con.commit()
    return result.lastrowid


def delete_file(file_name):
    cur.execute("""
    DELETE FROM izvestaj
    WHERE file_id = (
        SELECT id
        FROM file
        WHERE name = ?
    )""", [file_name])
    cur.execute("""
    DELETE FROM file
    WHERE name = ?""", [file_name])
    con.commit()


def save_resources(file_location, file_id):
    reports = excel_reader.read_from_excel(file_location, file_id)
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
        'neto',
        'file_id'
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", reports)
    con.commit()


def delete_all():
    cur.execute("delete from izvestaj;")
    con.commit()
