from gpgservice import GPGService

gpgService = GPGService()

# gpgService.generate_keys('test2')

# message = gpgService.encrypt_message('testowa wiadomosc','test2')

# print(message)

# decrypted = gpgService.decrypt_message(message)

# print(decrypted['data'])
# print('\n uuid :\n')
# print(decrypted['uuid'])

key = gpgService.get_public_key('test2')
