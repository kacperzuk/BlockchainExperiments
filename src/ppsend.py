#!/usr/bin/env python3 -bb

import time

import rethinkdb as r
from bigchaindb import Bigchain, crypto, util

class BBigchain(Bigchain):
    def get_genesis_block(self):
        return list(r.table('bigchain', read_mode=self.read_mode)
                    .filter(util.is_genesis_block)
                    .run(self.conn))[0]

    def get_transactions_since_block(self, block):
        blocks = (r.table('bigchain', read_mode=self.read_mode)
                     .filter(lambda b: b["block"]["timestamp"] > block["block"]["timestamp"])
                     .order_by(lambda b: b["block"]["timestamp"])
                     .run(self.conn))

        transactions = []
        last_block = block
        for block in blocks:
            last_block = block
            if self.block_election_status(block) == "valid":
                for tx in block["block"]["transactions"]:
                    transactions.append({ "message_id": tx["id"], "message": tx["transaction"]["data"]["payload"] })
        return transactions, last_block

def init():
    global bdb
    bdb = BBigchain()

def push_message_dict_to_bigchaindb(message):
    global bdb
    
    assert isinstance(message, dict)

    ephemeral_keypair = crypto.generate_key_pair()

    ctx = bdb.create_transaction(bdb.me, ephemeral_keypair[1], None, 'CREATE', payload=message); 
    ctx = bdb.sign_transaction(ctx, bdb.me_private)
    bdb.validate_transaction(ctx)
    bdb.write_transaction(ctx)

    return ctx["id"]


def get_message_status(message_id):
    """ possible returns: valid', 'undecided', 'backlog' or None """
    global bdb

    return bdb.get_status(message_id)

lblock = None
def read_message():
    global bdb, lblock

    if not lblock:
        lblock = bdb.get_genesis_block()

    transactions, lblock = bdb.get_transactions_since_block(lblock)
    for tx in transactions:
        print(tx)

if __name__ == "__main__":
    init()
    read_message()
    print("===============")
    read_message()
    print("===============")
    mid = push_message_dict_to_bigchaindb({"msg": "asjkdhajhsgd test!", "timestamp": time.time()})
    mid = push_message_dict_to_bigchaindb({"msg": "asjkdhajhsgd test!", "timestamp": time.time()})
    mid = push_message_dict_to_bigchaindb({"msg": "asjkdhajhsgd test!", "timestamp": time.time()})
    mid = push_message_dict_to_bigchaindb({"msg": "asjkdhajhsgd test!", "timestamp": time.time()})
    mid = push_message_dict_to_bigchaindb({"msg": "asjkdhajhsgd test!", "timestamp": time.time()})
    time.sleep(5)
    read_message()
    print("===============")
    read_message()
    print("===============")
    read_message()
