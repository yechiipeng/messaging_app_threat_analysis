# encrypt_send_demo.py
import json
from utils import make_shared_key, lock_message, to_text
from binascii import unhexlify

if __name__ == "__main__":
    a = json.load(open("clientA_keys.json"))
    b = json.load(open("clientB_keys.json"))
    a_sk = unhexlify(a["sk"])
    b_pk = unhexlify(b["pk"])

    session_key = make_shared_key(a_sk, b_pk)
    msg = b"hello, This is for Tojehova's cryptography class"
    nonce, ct = lock_message(session_key, msg, extra_data=b"A->B")
    envelope = {
        "from": "A",
        "to": "B",
        "nonce": nonce.hex(),
        "ciphertext": ct.hex()
    }
    open("envelope.json","w").write(json.dumps(envelope))
    print("Envelope written to envelope.json")
    print("Session key (base64):", to_text(session_key))
    print("Nonce (hex):", nonce.hex())
    print("Ciphertext (hex, truncated):", ct.hex()[:120], "...")
