import gnupg
import json
import pprint

class GPGService:

	def __init__(self):
		super(GPGService, self).__init__()
		self.gpg = gnupg.GPG(gnupghome ='homegpg')

		with open('keys.json','r') as dataFile: 
			self.keysFp = json.load(dataFile)

	def createKeys(self, domain):
		self.inputData = self.gpg.gen_key_input(
				name_email = domain,
				passphrase = 'password')

		key = self.gpg.gen_key(self.inputData)

		self.keysFp[domain] = key.fingerprint
		self.updateKeysFpFile()

	def encodeMessage(self, message, senderDomain):
		return str(self.gpg.encrypt(message, senderDomain))

	def decodeMessage(self, message):
		decryptedData = self.gpg.decrypt(message, passphrase ='password')
		return decryptedData.ok

	def printAllKeys(self):
		publicKeys = self.gpg.list_keys()
		privateKeys = self.gpg.list_keys(True)

		pprint.pprint(publicKeys)
		pprint.pprint(privateKeys)


	def removeKey(self, domain):
		print(str(self.gpg.delete_keys(self.keysFp[domain], True)))
		print(str(self.gpg.delete_keys(self.keysFp[domain])))
		self.keysFp.pop(domain)
		self.updateKeysFpFile()

	def savePublicKeyToFile(self, domain):
		publickKey = self.gpg.export_keys(self.keysFp[domain])
		filePath = 'exported_keys/' + domain + '.asc'
		with open(filePath,'w') as inputFile:
			inputFile.write(publickKey)
		return filePath

	def importPublicKeyFromFile(self, filePath, domain):
		keyData = open(filePath,'r').read()
		importResult = self.gpg.import_keys(keyData)

		print('imported:')
		pprint.pprint(importResult.fingerprints)

		if not importResult.fingerprints :
			self.keysFp[domain] = importResult.fingerprints[1]
			self.updateKeysFpFile()


	def updateKeysFpFile(self):
		with open('keys.json', 'w') as outfile:
			json.dump(self.keysFp, outfile)
