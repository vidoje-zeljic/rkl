CREATE TABLE "izvestaj" (
	"id"	INTEGER NOT NULL UNIQUE,
	"broj"	INTEGER NOT NULL UNIQUE,
	"datum"	TEXT NOT NULL,
	"posiljalac"	TEXT NOT NULL,
	"porucilac"	TEXT NOT NULL,
	"primalac"	TEXT NOT NULL,
	"artikal"	TEXT NOT NULL,
	"prevoznik"	TEXT NOT NULL,
	"registracija"	TEXT NOT NULL,
	"vozac"	TEXT NOT NULL,
	"bruto"	REAL NOT NULL,
	"tara"	REAL NOT NULL,
	"neto"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)