# wrong_key_decrypt.py
# Attempt to decrypt envelope.json with a wrong/private key to show confidentiality holds.
# Usage: python wrong_key_decrypt.py

import json
from binascii import unhexlify
from nacl.public import PrivateKey
from utils import make_shared_key, unlock_message

ENVELOPE = "envelope.json"
A_KEYS = "clientA_keys.json"

def load_a_pub(path):
    j = json.load(open(path))
    return unhexlify(j["pk"])

if __name__ == "__main__":
    # Load A's public key (the sender's public key)
    try:
        a_pub = load_a_pub(A_KEYS)
    except Exception as e:
        raise SystemExit(f"Failed to load {A_KEYS}: {e}")

    # Load envelope
    try:
        env = json.load(open(ENVELOPE))
        nonce = unhexlify(env["nonce"])
        ct = unhexlify(env["ciphertext"])
    except Exception as e:
        raise SystemExit(f"Failed to load {ENVELOPE}: {e}")

    # Generate a WRONG random X25519 private key (attacker has no relation to B)
    wrong_sk = PrivateKey.generate()
    wrong_sk_bytes = bytes(wrong_sk)

    # Derive session key using wrong private key and A's public key
    # This is what a wrong-key attacker would try
    try:
        session_key = make_shared_key(wrong_sk_bytes, a_pub)
        print("Derived session key (wrong key) (hex):", session_key.hex())
    except Exception as e:
        raise SystemExit(f"Failed deriving session key with wrong key: {e}")

    # Try to decrypt
    try:
        pt = unlock_message(session_key, nonce, ct, extra_data=b"A->B")
        print("Unexpected: decryption succeeded with wrong key! Plaintext:")
        print(pt.decode())
    except Exception as e:
        print("Failed: decryption with wrong key failed.")
        print("Exception:", repr(e))
