#!/usr/bin/env python3 -bb

from chain import MBigchain

class MsgHandler(object):
    def __init__(self):
        self.b = MBigchain()

    def check_messages(self):
        our_messages = []
        for msg in self.b.check_messages():
            #msg = gpgdecrypt(msg)
            if msg:
                our_messages.append(msg)
        return our_messages

    def push_message(self, message, recipient):
        msg = { "msg": message }
        #msg = {
        #    "msg": gpgencrypt(message, recipient)
        #}
        return self.b.push_message(msg)

if __name__ == "__main__":
    import time
    from pprint import pprint
    m = MsgHandler()
    print("Current messages:")
    pprint(m.check_messages())
    print("Pushing new message...")
    m.push_message({"HI": "HO"}, None)
    import time
    time.sleep(5)
    print("New messages:")
    pprint(m.check_messages())
