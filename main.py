import pyfiglet
import os
import util
import json
import sqlite3
from flask import Flask
from flask import render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask import send_file

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "foo": {
        "password": generate_password_hash("pass"),
        "roles": ["admin"]
    },
    "bar": {
        "password": generate_password_hash("pass"),
        "roles": ["read"]
    },
}


@app.route('/upload')
def main():
    return render_template("upload.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        # print(f.read().decode("utf-8"))
        f.save("uploads/" + f.filename)
        return render_template("upload-success.html", name=f.filename)


@app.route('/download')
def download_file ():
    path = "uploads/1.txt"
    return send_file(path, as_attachment=True)


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username)["password"], password):
        return username


@app.route("/")
def index():
    return render_template('index.html', jsonData=reports)


@app.route("/home")
# @auth.login_required
def home():
    # if 'admin' in users[auth.current_user()]['roles']:
    #     print("ok")
    # else:
    #     print("error")
    date = request.args.get('date')
    time = request.args.get('time')
    if time is not None:
        print(time)
    else:
        print("Time is None")
    return f"Hello, {date}"
    # return "Hello, {}!".format(auth.current_user())
    # return render_template('home.html', jsonData=reports)


print(pyfiglet.figlet_format("RKL"))


reports = []

# csv_dir = os.fsencode("resources/csv")
#
# for csv_file in os.listdir(csv_dir):
#     reports.extend(util.read_reports_from_csv(f"resources/csv/{os.fsdecode(csv_file)}"))


# print(json.dumps(reports, indent=4))
# reports = util.prepare_for_insert(reports)
# print(reports)
con = sqlite3.connect("resources/db/tutorial.db")
cur = con.cursor()

res = cur.execute("select * from izvestaj;")

# print(res.fetchall())
reports = util.db_json_mapper(res)
# print(json.dumps(reports, indent=4))
#
# cur.executemany("""
#     INSERT INTO izvestaj ('broj', 'datum', 'posiljalac', 'porucilac', 'primalac', 'artikal', 'prevoznik', 'registracija', 'vozac', 'bruto', 'tara', 'neto')
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", reports)
#
# con.commit()
