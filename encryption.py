from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import base64


def encrypt_message(message):
  #public key
  with open("./public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(key_file.read(),
                                                   backend=default_backend())
    ciphertext = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None))

    return base64.b64encode(ciphertext).decode('utf-8')


def decrypt_message(ciphertext):
  ciphertext = base64.b64decode(ciphertext)
  # print("debug1: ",ciphertext)
  with open("./private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

  # print("debug2")
  plaintext = private_key.decrypt( ciphertext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                   algorithm=hashes.SHA256(),
                   label=None))

  # print("debug3 : ", plaintext)

  return plaintext.decode('utf-8')

def fetchPubKey():
  with open("./public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

  stringKey = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')

  return stringKey