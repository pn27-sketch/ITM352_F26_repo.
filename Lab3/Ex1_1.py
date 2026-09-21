from cryptography.fernet import Fernet

#generate a key for encryption and decryption
key = Fernet.generate_key()
f = Fernet(key)

#get input from the user
message = input("Enter a string to encrypt: ")
message_bytes = message.encode()

#Encrypt the message and then decrypt it
encrypted_message = f.encrypt(message_bytes)
decrypted_message = f.decrypt(encrypted_message)
print("Encrypted:", encrypted_message)
print("Decrypted:", decrypted_message.decode())