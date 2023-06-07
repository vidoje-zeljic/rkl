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


@app.route("/delete")
@auth.login_required
def delete():
    db.delete_all()
    return "Success"


@app.route("/")
@auth.login_required
def index():
    print(auth)
    return render_template('index.html', user=auth.current_user())


@app.route("/reports")
@auth.login_required
def reports():
    return render_template('reports.html', reports=db.get_resources())


@app.route('/upload', methods=['GET', 'POST'])
@auth.login_required
def upload():
    if request.method == 'GET':
        return render_template("upload.html")
    if request.method == 'POST':
        f = request.files['file']
        file_location = "./uploads/" + f.filename
        f.save(file_location)
        db.save_resources(file_location)
        return render_template("upload-success.html", name=f.filename)


@app.route('/files')
@auth.login_required
def files():
    uploads = os.fsencode("./uploads")
    files = []
    for file in os.listdir(uploads):
        files.append(os.fsdecode(file))
    return render_template("files.html", files=files)


@app.route('/files/<file_name>')
@auth.login_required
def file_download(file_name):
    return send_file("./uploads/" + file_name, as_attachment=True)
