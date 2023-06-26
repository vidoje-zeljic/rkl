import os

from flask import Flask, render_template, request, send_file
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

import db
import db_util
import excel_util
import security

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username in security.users and check_password_hash(security.users.get(username)["password"], password):
        return username


@app.route("/")
@auth.login_required
def index():
    print(auth)
    return render_template('index.html', user=auth.current_user())


@app.route("/reports", methods=['GET', 'POST'])
@auth.login_required
def reports():
    broj = None if 'broj' not in request.args else request.args['broj']
    neto_od = None if 'neto-od' not in request.args else request.args['neto-od']
    neto_do = None if 'neto-do' not in request.args else request.args['neto-do']
    posiljalac = None if 'posiljalac' not in request.args else request.args['posiljalac']
    porucilac = None if 'porucilac' not in request.args else request.args['porucilac']
    primalac = None if 'primalac' not in request.args else request.args['primalac']
    artikal = None if 'artikal' not in request.args else request.args['artikal']
    prevoznik = None if 'prevoznik' not in request.args else request.args['prevoznik']
    registracija = None if 'registracija' not in request.args else request.args['registracija']
    datum_od = None if 'datum-od' not in request.args else request.args['datum-od']
    datum_do = None if 'datum-do' not in request.args else request.args['datum-do']
    limit = 1
    if datum_od is not None or datum_do is not None:
        limit = -1
    elif 'limit' in request.args:
        limit = int(request.args['limit'])

    vreme_checkbox = 'false' if 'vreme-checkbox' not in request.args else request.args['vreme-checkbox']
    primalac_checkbox = 'false' if 'primalac-checkbox' not in request.args else request.args['primalac-checkbox']
    vozac_checkbox = 'false' if 'vozac-checkbox' not in request.args else request.args['vozac-checkbox']
    bruto_checkbox = 'false' if 'bruto-checkbox' not in request.args else request.args['bruto-checkbox']
    tara_checkbox = 'false' if 'tara-checkbox' not in request.args else request.args['tara-checkbox']
    optional_columns = {
        'vreme': vreme_checkbox,
        'primalac': primalac_checkbox,
        'vozac': vozac_checkbox,
        'bruto': bruto_checkbox,
        'tara': tara_checkbox,
    }

    db_resoults = db.get_resources(limit, broj, neto_od, neto_do, posiljalac, porucilac, primalac, artikal, prevoznik,
                                   registracija, datum_od, datum_do)

    if request.method == 'GET':
        return render_template('reports.html',
                               count=db_resoults[1],
                               neto_sum=db_util.format_number(db_resoults[2]),
                               reports=db_resoults[0],
                               posiljaoci=db.posiljaoci(),
                               porucioci=db.porucioci(),
                               primaoci=db.primaoci(),
                               artikli=db.artikli(),
                               prevoznici=db.prevoznici(),
                               registracije=db.registracije(),
                               broj=broj,
                               neto_od=neto_od,
                               neto_do=neto_do,
                               posiljalac=posiljalac,
                               porucilac=porucilac,
                               primalac=primalac,
                               artikal=artikal,
                               prevoznik=prevoznik,
                               registracija=registracija,
                               datumOd=datum_od,
                               datumDo=datum_do,
                               limit=limit,
                               optionalColumns=optional_columns
                               )

    if request.method == 'POST':
        folder_name = 'exports/'
        file_name = 'export.xlsx'
        excel_util.export_to_excel(folder_name + file_name, db_resoults[0])
        return file_name


@app.route('/files', methods=['GET', 'POST'])
@auth.login_required
def files():
    if request.method == 'GET':
        return render_template("files.html", files=db.get_files())

    if request.method == 'POST':
        f = request.files['file']
        if db.get_file_by_name(f.filename):
            db.delete_file(f.filename)
        file_location = "./uploads/" + f.filename
        f.save(file_location)
        file_id = db.save_file(f.filename)
        db.save_resources(file_location, file_id)
        return render_template("files.html", files=db.get_files(), uploaded_file=f.filename)


@app.route('/files/<file_name>', methods=['GET', 'DELETE'])
@auth.login_required
def file(file_name):
    if request.method == 'GET':
        return send_file("./uploads/" + file_name, as_attachment=True)

    if request.method == 'DELETE':
        os.remove("uploads/" + file_name)
        db.delete_file(file_name)
        return "OK"


@app.route('/exports/<file_name>', methods=['GET', 'DELETE'])
@auth.login_required
def exports(file_name):
    if request.method == 'GET':
        return send_file("./exports/" + file_name, as_attachment=True)

    if request.method == 'DELETE':
        os.remove("exports/" + file_name)
        db.delete_file(file_name)
        return "OK"


@app.route("/finance")
@auth.login_required
def finance():
    return render_template('finance.html',
                           prices=db.pricesJson(),
                           posiljaoci=db.posiljaoci(),
                           artikli=db.artikli(),
                           mesta=db.mesta(),
                           )


@app.route("/prices", methods=["POST"])
@auth.login_required
def create_price():
    db.save_price(request.json)
    return "OK"


def get_files():
    uploads = os.fsencode("./uploads")
    files = []
    for file in os.listdir(uploads):
        files.append(os.fsdecode(file))
    return files


app.run()
