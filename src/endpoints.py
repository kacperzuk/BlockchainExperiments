from flask import render_template
from main import app

@app.route("/")
def hello(name=None):
    return render_template("main.html", name=name)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/rcv_form")
def receive():
    return render_template("rcv_form.html")

@app.route("/snd_form")
def show_names():
    db = get_db()
    cur = db.execute("select name from contacts")
    names = cur.fetchall()
    return render_template("snd_form.html", names=names)

#@app.route("/contact_form", methods=["POST"])
#def add_name():
#    db = get_db()
#    db.execute("insert into contacts( name ) values (?)", request.form["contact_name"]])
#    db.commit()
#    flash("New entry was successfully posted")
#  # return redirect(url_for("show_names"))
#    return render_template("contact_form.html")

@app.route("/contact_form")
def add_name():
    return render_template("contact_form.html")

@app.route("/", methods=("POST",))
def add_rec():
    contact_name = request.form["contact_name"]
    fingerprint = request.form["fingerprint"]
    cur = get_db().cursor()
    query = "INSERT INTO contacts (name, fingerprint) VALUES (?, ?)"
    cur.execute(query, (contact_name, fingerprint))

    return render_template("main.html")
