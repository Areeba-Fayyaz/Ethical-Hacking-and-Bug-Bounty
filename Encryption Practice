
# Base64 is a binary-to-text encoding scheme that represents binary data in an ASCII string format.
import base64

# encrypt_password function is used to encode password given to this function
def encrypt_password(password):
    encrypted_bytes = base64.b64encode(password.encode())
    return encrypted_bytes

# decrypt_password function is used to decode encrypted password given to this function
def decrypt_password(encoded_password):
    decrypted_bytes = base64.b64decode(encoded_password)
    return decrypted_bytes

print(encrypt_password('pass'))
print(decrypt_password(encrypt_password('pass')))
