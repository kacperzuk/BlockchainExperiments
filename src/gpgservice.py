import gnupg  
import re

class GPGService:

	def __init__(self):
		self.gpg = gnupg.GPG(gnupghome = 'homegpg')
		self.gpg.encoding = 'utf-8'

	def generate_keys(self, uuid):
		 self.gpg.gen_key(self.gpg.gen_key_input(name_email = uuid))

	def get_public_key(self, uuid):
		return self.gpg.export_keys(uuid)

	def add_conversation(self, uuid, public_key):
		import_result = self.gpg.import_keys(public_key)
		if bool(import_result.results[0]['ok']):
			return True
		else:
			return False

	def encrypt_message(self, message, uuid):
		message_params = {}
		message_params['data'] = message
		message_params['fingerprint'] = self._get_fingerprint_for_key(uuid)
		return self.gpg.encrypt(str(message_params), uuid)

	def decrypt_message(self, encrypted):
		result = {}
		decrypted_data = self.gpg.decrypt(str(encrypted))
		decrypted_data = eval(str(decrypted_data))
		result['data'] = decrypted_data['data']
		result['uuid'] = self._get_uuid_from_key(decrypted_data['fingerprint'])
		return result

	def _get_uuid_from_key(self, fingerprint):
		public_keys = self.gpg.list_keys()
		for key in public_keys:
			if fingerprint in key['fingerprint']:
				result = re.search('<(.*?)>',key['uids'][0])
				return result.group(1)

	def _get_fingerprint_for_key(self, uuid):
		public_keys = self.gpg.list_keys()
		for key in public_keys:
			if uuid in key['uids'][0]:
				return key['fingerprint']






