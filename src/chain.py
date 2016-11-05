#!/usr/bin/env python3 -bb

import pickle
import rethinkdb as r
from bigchaindb import Bigchain, crypto, util

class MBigchain(Bigchain):
    def __init__(self):
        super(MBigchain, self).__init__()
        try:
            with open('data/last_block', 'rb') as f:
                self.last_block = pickle.load(f)
        except (FileNotFoundError,pickle.UnpicklingError,EOFError):
            self.last_block = None

    def _get_genesis_block(self):
        return list(r.table('bigchain', read_mode=self.read_mode)
                    .filter(util.is_genesis_block)
                    .run(self.conn))[0]

    def _get_transactions_since_block(self, block):
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
                    transactions.append(tx)
        return transactions, last_block

    def _set_last_block(self, last_block):
        self.last_block = last_block
        with open('data/last_block', 'wb') as f:
            pickle.dump(last_block, f)

    """ PUBLIC METHODS BELOW """

    def push_message(self, message):
        assert isinstance(message, dict)

        ephemeral_keypair = crypto.generate_key_pair()

        ctx = self.create_transaction(self.me, ephemeral_keypair[1], None, 'CREATE', payload=message); 
        ctx = self.sign_transaction(ctx, self.me_private)
        self.validate_transaction(ctx)
        self.write_transaction(ctx)

        return ctx["id"]

    def get_message_status(self, message_id):
        """ possible returns: valid', 'undecided', 'backlog' or None """
        return self.get_status(message_id)

    def check_messages(self, from_beginning=False):
        if not self.last_block or from_beginning:
            self._set_last_block(self._get_genesis_block())

        transactions, last_block = self._get_transactions_since_block(self.last_block)
        self._set_last_block(last_block)

        transactions = [{ "message_id": tx["id"], "message": tx["transaction"]["data"]["payload"] } for tx in transactions]

        return transactions


if __name__ == "__main__":
    b = MBigchain()
    print("Current messages:")
    pprint(b.check_messages())
    print("Pushing new message...")
    b.push_message({"HI": "HO"})
    from pprint import pprint
    import time
    time.sleep(5)
    print("New messages:")
    pprint(b.check_messages())
