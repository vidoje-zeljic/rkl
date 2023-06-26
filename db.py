import sqlite3
from datetime import datetime

import db_util
import excel_util

DT_FORMAT = "%Y-%m-%d %H:%M:%S"

con = sqlite3.connect("./rkl.db", check_same_thread=False)
cur = con.cursor()


def get_all_resources():
    res = cur.execute("select * from izvestaj;")
    return db_util.db_json_mapper(res)


def get_resources(limit, broj, neto_od, neto_do, posiljalac, porucilac, primalac, artikal, prevoznik, registracija,
                  datum_od,
                  datum_do):
    query = """
    SELECT {select}
    FROM izvestaj i
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
        (? is null or ? <= neto) AND
        datum in (  
            SELECT DISTINCT datum
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
            ORDER BY datum desc
            LIMIT ?
        )
    ORDER BY broj DESC
    """
    params = [broj, broj, datum_do, datum_do, datum_od, datum_od, posiljalac, posiljalac, porucilac,
              porucilac, primalac, primalac, artikal, artikal, prevoznik, prevoznik, registracija,
              registracija, neto_do, neto_do, neto_od, neto_od, broj, broj, datum_do, datum_do, datum_od,
              datum_od, posiljalac, posiljalac, porucilac,
              porucilac, primalac, primalac, artikal, artikal, prevoznik, prevoznik, registracija,
              registracija, neto_do, neto_do, neto_od, neto_od, limit]

    cnt = cur.execute(query.format(select="count(1)"), params).fetchall()[0][0]
    neto_sum = cur.execute(query.format(select="sum(neto)"), params).fetchall()[0][0]
    neto_sum = 0 if neto_sum is None else neto_sum
    cena_sql = """
    CASE
        WHEN mesto is null
            THEN 0
        ELSE (
            select c.cena * i.neto
            from cena c
            where
                c.datum_od <= i.datum
                and c.porucilac = i.porucilac
                and c.artikal = i.artikal
                and c.mesto = i.mesto
            order by c.datum_od desc
            limit 1
        )
    END"""
    izvestaj_cena_select = f"""*,
    {cena_sql} AS cena"""
    sum_izvestaj_cena_select = f"""SUM({cena_sql}) AS cena"""
    cena_sum = cur.execute(query.format(select=sum_izvestaj_cena_select), params).fetchall()[0][0]
    cena_sum = 0 if cena_sum is None else cena_sum
    res = cur.execute(query.format(select=izvestaj_cena_select), params)
    return db_util.db_json_mapper(res), cnt, neto_sum, cena_sum


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


def mesta():
    return cur.execute("select distinct mesto from izvestaj where mesto is not null order by mesto asc").fetchall()


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
    reports = excel_util.read_from_excel(file_location, file_id)
    cur.executemany("""
    INSERT INTO izvestaj(
        'broj',
        'datum',
        'vreme',
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
        'mesto',
        'file_id'
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", reports)
    con.commit()


def save_price(price):
    cur.execute("""
    INSERT INTO cena(
        'datum_od',
        'porucilac',
        'artikal',
        'mesto',
        'cena'
    )
    VALUES (?, ?, ?, ?, ?)""", list(price.values()))
    con.commit()


def delete_price(id):
    cur.execute("""
    DELETE FROM cena
    WHERE id = ?""", [id])
    con.commit()


def prices():
    return cur.execute("select * from cena").fetchall()


def pricesJson():
    prices = cur.execute("select * from cena").fetchall()
    pricesJson = []
    for price in prices:
        priceJson = {
            "id": price[0],
            "datum-od": price[1],
            "posiljalac": price[2],
            "artikal": price[3],
            "mesto": price[4],
            "cena": price[5],
        }
        pricesJson.append(priceJson)
    return pricesJson
