from flask import render_template, request, redirect, url_for

from main import app
from connectors import get_db, get_chain, get_gpg

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

@app.route("/snd_form", methods=("POST",))
def send_message():
    # get details
    message = request.form["text"]
    contact = request.form["contact"]

    # get fingerprint for this contact
    db = get_db()
    cur = db.execute("select fingerprint from contacts where name = ?", (contact,))
    fingerprint = cur.fetchall()[0][0]

    # encrypt message
    encrypted = get_gpg().encrypt_message(message, fingerprint)

    # pass message to chain
    get_chain().push_message(encrypted)

    return redirect(url_for('show_names'))

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

@app.route("/add_rec", methods=("POST",))
def add_rec():
    contact_name = request.form["contact_name"]
    public_key = request.form["public_key"]
    fingerprint = get_gpg().add_contact(public_key)
    if not fingerprint:
        return "Invalid public key!"

    con = get_db()
    query = "insert into contacts (name, fingerprint) values (?, ?)"
    con.execute(query, (contact_name, fingerprint))
    con.commit()

    return redirect(url_for("main"))
