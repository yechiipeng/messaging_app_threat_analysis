# Helper functions for secure messaging
import os, base64
from nacl.public import PrivateKey, PublicKey
from nacl.bindings import crypto_scalarmult
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

# to generate x25519 keypair s
def create_keys():
    private_key = PrivateKey.generate()
    public_key = private_key.public_key
    return private_key, public_key

# key conversion into bytes
def key_to_bytes(key):
    return bytes(key)

#create shared key from A_priv, B_pub using HKDF
def make_shared_key(my_private, their_public):
    shared_secret = crypto_scalarmult(my_private, their_public)
    key_maker = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'session')
    return key_maker.derive(shared_secret)

#encrypt message
def lock_message(key, message, extra_data=None):
    cipher = ChaCha20Poly1305(key)
    random_nonce = os.urandom(12)
    encrypted = cipher.encrypt(random_nonce, message, extra_data)
    return random_nonce, encrypted

#decrypt message
def unlock_message(key, nonce, encrypted_msg, extra_data=None):
    cipher = ChaCha20Poly1305(key)
    return cipher.decrypt(nonce, encrypted_msg, extra_data)


def to_text(data):
    return base64.b64encode(data).decode()

def from_text(text):
    return base64.b64decode(text)
