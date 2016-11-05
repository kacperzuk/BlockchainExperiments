from flask import render_template, request, redirect, url_for

from main import app
from connectors import get_db, get_chain, get_gpg

@app.route("/")
def main():
    db = get_db()
    fingerprint = db.execute("select value from settings where name = 'pubkey'").fetchall()
    if not fingerprint:
        query = "insert into settings (name, value) VALUES ('pubkey', ?)"
        fingerprint = get_gpg().generate_key_pair()
        if not fingerprint:
            print(fingerprint)
            return "wtf"
        db.execute(query, (fingerprint,))
        db.commit()
    else:
        fingerprint = fingerprint[0][0]

    my_pub_key = get_gpg().get_public_key(fingerprint)
    return render_template("main.html", pkey=my_pub_key)

@app.route("/rcv_form")
def receive():
    chain_messages = [ m["message"] for m in get_chain().check_messages() ]
    decrypted_messages = [ get_gpg().decrypt_message(m) for m in chain_messages ]
    valid_messages = [ m for m in decrypted_messages if m ]
    return render_template("rcv_form.html", messages=valid_messages)

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
