from gpgservice import GPGService

gpgService = GPGService()

# gpgService.createKeys('test1@gmail.com')

# gpgService.createKeys('test2@gmail.com')

# message = gpgService.encodeMessage('testowa wiadomosc','test2@gmail.com')

# decryptedStatus = gpgService.decodeMessage(message)

# print ('ok: ', decryptedStatus)
# print ('status: ', decrypted.status)
# print ('stderr: ', decrypted.stderr)
# print ('decrypted string: ', decrypted.data)



# gpgService.removeKey('test2@gmail.com')
# gpgService.removeKey('test1@gmail.com')


gpgService.savePublicKeyToFile('test2@gmail.com')
# gpgService.importPublicKeyFromFile('test2@gmail.com.asc','test2@gmail.com')

gpgService.printAllKeys()