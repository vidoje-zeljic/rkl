import os

from flask import Flask, render_template, request, send_file
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

import db
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


@app.route("/reports")
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
    datumOd = None if 'datum-od' not in request.args else request.args['datum-od']
    datumDo = None if 'datum-do' not in request.args else request.args['datum-do']
    return render_template('reports.html',
                           reports=db.get_resources(),
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
                           datumOd=datumOd,
                           datumDo=datumDo
                           )


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


def get_files():
    uploads = os.fsencode("./uploads")
    files = []
    for file in os.listdir(uploads):
        files.append(os.fsdecode(file))
    return files
