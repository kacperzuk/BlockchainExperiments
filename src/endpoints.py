import datetime
import json

from flask import render_template, request, redirect, url_for

from main import app
from connectors import get_db, get_chain, get_gpg

def recv_messages():
    chain_messages = [ m["message"] for m in get_chain().check_messages() ]
    decrypted_messages = [ get_gpg().decrypt_message(m) for m in chain_messages ]
    valid_messages = [ m for m in decrypted_messages if m ]

    for i in valid_messages:
        db = get_db()
        data = json.loads(i["data"])
        cur = db.execute("select id from conversation where our_next_fingerprint = ?", (i["fingerprint"],))
        try:
            cid = cur.fetchall()[0][0]
        except IndexError:
            continue
        time = "{:%c}".format(datetime.datetime.now())
        next_fingerprint = get_gpg().add_contact(data["next_pubkey"])
        db.execute("insert into message (incoming, conversation_id, content, datetime) values (1, ?,?,?)", (cid, data["message"], time))
        db.execute("update conversation set message_count = message_count + 1, last_message_time = ?, their_next_fingerprint = ? where id = ?", (time,next_fingerprint,cid))
        db.commit()

@app.route("/")
def main():
    recv_messages()
    db = get_db()
    cur = db.execute("select * from conversation order by case when last_message_time is null then 1 else 0 end desc, last_message_time desc");
    conversations = cur.fetchall()
    return render_template("main.html", conversations=conversations)

@app.route("/start_conversation")
def start_conversation():
    return render_template("start_conversation.html")

@app.route("/start_conversation", methods=["POST"])
def create_conversation():
    db = get_db()
    name = request.form["name"].strip()
    their_pubkey = request.form["public_key"].strip()
    our_pubkey = get_gpg().generate_key_pair()
    query = "insert into conversation (name, our_next_fingerprint, their_next_fingerprint) values (?, ?, ?)"

    if their_pubkey:
        their_pubkey = get_gpg().add_contact(their_pubkey)

    db.execute(query, (name, our_pubkey, their_pubkey))
    db.commit()

    return redirect(url_for("main"))

@app.route("/conversation/<int:cid>")
def conversation(cid):
    def dict_from_row(row):
        return dict(zip(row.keys(), row))       
    recv_messages()
    db = get_db()
    cur = db.execute("select * from conversation where id = ?", (cid,))
    conversation = dict_from_row(cur.fetchall()[0])
    conversation["our_next_pubkey"] = get_gpg().get_public_key(conversation["our_next_fingerprint"])

    cur = db.execute("select * from message where conversation_id = ? order by id desc", (cid,))
    messages = cur.fetchall()
    return render_template("conversation.html", conversation=conversation, messages=messages)

@app.route("/conversation/<int:cid>", methods=["POST"])
def send_message(cid):
    message = request.form["text"]

    # get fingerprint for this conversation
    db = get_db()
    cur = db.execute("select their_next_fingerprint from conversation where id = ?", (cid,))
    fingerprint = cur.fetchall()[0][0]

    our_next_fingerprint = get_gpg().generate_key_pair()
    wrapped_message = json.dumps({
        "next_pubkey": get_gpg().get_public_key(our_next_fingerprint),
        "message": message
    })

    # encrypt message
    encrypted = get_gpg().encrypt_message(wrapped_message, fingerprint)

    # pass message to chain
    get_chain().push_message(encrypted)
    time = "{:%c}".format(datetime.datetime.now())
    db.execute("update conversation set message_count = message_count + 1, last_message_time = ?, our_next_fingerprint = ?, their_next_fingerprint = null where id = ?", (time, our_next_fingerprint, cid))
    db.execute("insert into message (conversation_id, content, datetime) values (?, ?, ?)", (cid, message, time))
    db.commit()

    return redirect(url_for("conversation", cid=cid))
