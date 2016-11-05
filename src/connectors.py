from flask import g

def get_gpg():
    if not hasattr(g, 'gpg'):
        g.gpg = GPGService()
    return g.gpg

def get_chain():
    if not hasattr(g, 'chain'):
        g.chain = MBigchain()
    return g.chain

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

from db import connect_db
from chain import MBigchain
from gpg_service import GPGService
