# decrypt_receive_demo.py
import json
from utils import make_shared_key, unlock_message
from binascii import unhexlify

if __name__ == "__main__":
    a = json.load(open("clientA_keys.json"))
    b = json.load(open("clientB_keys.json"))
    env = json.load(open("envelope.json"))

    b_sk = unhexlify(b["sk"])
    a_pk = unhexlify(a["pk"])

    session_key = make_shared_key(b_sk, a_pk)
    nonce = unhexlify(env["nonce"])
    ct = unhexlify(env["ciphertext"])
    pt = unlock_message(session_key, nonce, ct, extra_data=b"A->B")
    print("Decrypted plaintext:", pt.decode())
