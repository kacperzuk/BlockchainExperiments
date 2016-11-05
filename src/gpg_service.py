import gnupg
import json

def monkey_patch_for_genkey_handle_status(self, key, value):
    if key in ("PROGRESS", "GOOD_PASSPHRASE", "NODATA", "KEY_NOT_CREATED",
               "PINENTRY_LAUNCHED", "KEY_CONSIDERED"):
        pass
    elif key == "KEY_CREATED":
        (self.type,self.fingerprint) = value.split()
    else:
        raise ValueError("Unknown status message: %r" % key)

def monkey_patch_for_importresult_handle_status(self, key, value):
    try:
        if key == "IMPORT_OK":
            fingerprint = value.split(' ')[1]
            try:
                if not fingerprint in self.fixed_fingerprints:
                    self.fixed_fingerprints.append(fingerprint)
            except AttributeError:
                self.fixed_fingerprints = [fingerprint]

        return gnupg.ImportResult.handle_status(self, key, value)
    except:
        pass

gnupg.GenKey.handle_status = monkey_patch_for_genkey_handle_status
gnupg.ImportResult.handle_status = monkey_patch_for_importresult_handle_status

class GPGService:
    def __init__(self):
        self.gpg = gnupg.GPG(gnupghome = 'data/homegpg')
        self.gpg.encoding = 'utf-8'

    def generate_key_pair(self):
        key_input = self.gpg.gen_key_input(name_email = '', passphrase = "1")
        key = self.gpg.gen_key(key_input)
        return key.fingerprint

    def get_public_key(self, fingerprint):
        return self.gpg.export_keys(fingerprint)

    def add_contact(self, public_key):
        public_key = public_key.strip()
        import_result = self.gpg.import_keys(public_key.strip())
        if len(import_result.fixed_fingerprints) > 0:
            return import_result.fixed_fingerprints[0]
        else:
            return None

    def encrypt_message(self, message, fingerprint):
        message_params = {}
        message_params['data'] = message
        message_params['fingerprint'] = fingerprint
        encrypted = self.gpg.encrypt(json.dumps(message_params), fingerprint, always_trust=True)
        return str(encrypted)

    def decrypt_message(self, encrypted):
        decrypted_data = self.gpg.decrypt(encrypted, passphrase="1")
        decrypted_data = str(decrypted_data)
        if decrypted_data:
            return json.loads(decrypted_data)
        return None
