import gnupg
import json
import pprint

class GPGService:

	def __init__(self):
		super(GPGService, self).__init__()
		self.gpg = gnupg.GPG(gnupghome ='homegpg')
		with open('keys.json','r') as dataFile: 
			self.keysFp = json.load(dataFile)

	def createKey(self,email):
		self.inputData = self.gpg.gen_key_input(
				name_email= email,
				passphrase= 'password')

		key = self.gpg.gen_key(self.inputData)

		self.keysFp[email] = key.fingerprint
		self.updateKeysFpFile()

	def encodeMessage(self,message,senderDomain):
		return str(self.gpg.encrypt(message,senderDomain))

	def decodeMessage(self,message):
		decryptedData = self.gpg.decrypt(message,passphrase='password')
		return decryptedData.ok

	def printAllKeys(self):
		publicKeys = self.gpg.list_keys()
		privateKeys = self.gpg.list_keys(True)

		pprint.pprint(publicKeys)
		pprint.pprint(privateKeys)


	def removeKey(self,email):
		print(str(self.gpg.delete_keys(self.keysFp[email],True)))
		print(str(self.gpg.delete_keys(self.keysFp[email])))
		self.keysFp.pop(email)
		self.updateKeysFpFile()

	def updateKeysFpFile(self):
		with open('keys.json', 'w') as outfile:
			json.dump(self.keysFp, outfile)
