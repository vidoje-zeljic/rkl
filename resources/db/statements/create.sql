CREATE TABLE "file"
(
    "id"        INTEGER NOT NULL UNIQUE,
    "name"      TEXT    NOT NULL UNIQUE,
    "upload_dt" TEXT    NOT NULL,
    PRIMARY KEY ("id" AUTOINCREMENT)
);

insert into file(name)
values ('f1.txt');

INSERT INTO izvestaj('broj', 'datum', 'posiljalac', 'porucilac', 'primalac', 'artikal', 'prevoznik', 'registracija',
    'vozac', 'bruto', 'tara', 'neto', 'file_id')
VALUES (1, '2020-10-10', 'posiljalac1', 'porucilac1', 'primalac1', 'artikal1', 'prevoznik1', 'registracija1', 'vozac1',
        1000, 500, 200, 2)

CREATE TABLE "izvestaj"
(
    "id"           INTEGER NOT NULL UNIQUE,
    "broj"         INTEGER NOT NULL,
    "datum"        TEXT    NOT NULL,
    "vreme"        TEXT    NOT NULL,
    "posiljalac"   TEXT    NOT NULL,
    "porucilac"    TEXT    NOT NULL,
    "primalac"     TEXT    NOT NULL,
    "artikal"      TEXT    NOT NULL,
    "prevoznik"    TEXT    NOT NULL,
    "registracija" TEXT    NOT NULL,
    "vozac"        TEXT    NOT NULL,
    "bruto"        REAL    NOT NULL,
    "tara"         REAL    NOT NULL,
    "neto"         REAL    NOT NULL,
    "mesto"        TEXT    NOT NULL,
    "file_id"      INTEGER,
    PRIMARY KEY ("id" AUTOINCREMENT),
    FOREIGN KEY ("file_id") REFERENCES "file"
);

create table cena
(
    id         integer not null /*autoincrement needs PK*/,
    datum_od   TEXT    not null,
    porucilac  TEXT    not null,
    artikal    TEXT    not null,
    mesto      TEXT    not null,
    cena       integer not null
);
