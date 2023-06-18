import sqlite3
from datetime import datetime

import db_util
import excel_reader

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


def get_all_resources():
    res = cur.execute("select * from izvestaj;")
    return db_util.db_json_mapper(res)


def get_resources(broj, neto_od, neto_do, posiljalac, porucilac, primalac, artikal, prevoznik, registracija, datum_od,
                  datum_do):
    query = """
    SELECT {select}
    FROM izvestaj
    WHERE
        (? is null or ? = broj) AND
        (? is null or ? >= datum) AND
        (? is null or ? <= datum) AND
        (? is null or ? = posiljalac) AND
        (? is null or ? = porucilac) AND
        (? is null or ? = primalac) AND
        (? is null or ? = artikal) AND
        (? is null or ? = prevoznik) AND
        (? is null or ? = registracija) AND
        (? is null or ? >= neto) AND
        (? is null or ? <= neto)
    """

    cnt = cur.execute(query.format(select="count(1)"),
                      [broj, broj, datum_do, datum_do, datum_od, datum_od, posiljalac, posiljalac, porucilac,
                       porucilac, primalac, primalac, artikal, artikal, prevoznik, prevoznik, registracija,
                       registracija, neto_do, neto_do, neto_od, neto_od]
                      ).fetchall()[0][0]
    neto_sum = cur.execute(query.format(select="sum(neto)"),
                      [broj, broj, datum_do, datum_do, datum_od, datum_od, posiljalac, posiljalac, porucilac,
                       porucilac, primalac, primalac, artikal, artikal, prevoznik, prevoznik, registracija,
                       registracija, neto_do, neto_do, neto_od, neto_od]
                      ).fetchall()[0][0]
    neto_sum = 0 if neto_sum is None else neto_sum
    res = cur.execute(query.format(select="*"),
                      [broj, broj, datum_do, datum_do, datum_od, datum_od, posiljalac, posiljalac, porucilac,
                       porucilac, primalac, primalac, artikal, artikal, prevoznik, prevoznik, registracija,
                       registracija, neto_do, neto_do, neto_od, neto_od])
    return db_util.db_json_mapper(res), cnt, neto_sum


def get_files():
    return cur.execute("select * from file;").fetchall()


def get_file_by_name(file_name):
    return cur.execute("select * from file where name = ?", [file_name]).fetchall()


def posiljaoci():
    return cur.execute("select distinct posiljalac from izvestaj order by posiljalac asc").fetchall()


def porucioci():
    return cur.execute("select distinct porucilac from izvestaj order by porucilac asc").fetchall()


def primaoci():
    return cur.execute("select distinct primalac from izvestaj order by primalac asc").fetchall()


def artikli():
    return cur.execute("select distinct artikal from izvestaj order by artikal asc").fetchall()


def prevoznici():
    return cur.execute("select distinct prevoznik from izvestaj order by prevoznik asc").fetchall()


def registracije():
    return cur.execute("select distinct registracija from izvestaj order by registracija asc").fetchall()


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
