import gnupg
import json

class GPGService:
    def __init__(self):
        self.gpg = gnupg.GPG(gnupghome = 'data/homegpg')
        self.gpg.encoding = 'utf-8'

    def generate_key_pair(self):
        key = self.gpg.gen_key(self.gpg.gen_key_input(name_email = ''))
        return key.fingerprint

    def get_public_key(self, fingerprint):
        return self.gpg.export_keys(fingerprint)

    def add_contact(self, public_key):
        import_result = self.gpg.import_keys(public_key)
        return import_result.fingerprints[0]

    def encrypt_message(self, message, fingerprint):
        message_params = {}
        message_params['data'] = message
        message_params['fingerprint'] = fingerprint
        return str(self.gpg.encrypt(json.dumps(message_params), fingerprint))

    def decrypt_message(self, encrypted):
        decrypted_data = self.gpg.decrypt(encrypted)
        decrypted_data = json.loads(str(decrypted_data))
        return decrypted_data
