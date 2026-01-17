# forward_secrecy_demo.py
# Demonstrate lack of forward secrecy: stealing A's long-term private key decrypts prior messages.

import json, os, shutil
from binascii import unhexlify
from utils import make_shared_key, lock_message, unlock_message, create_keys, key_to_bytes

A_KEYS = "clientA_keys.json"
B_KEYS = "clientB_keys.json"

def write_envelope(msg, outfile="envelope.json"):
    with open(A_KEYS) as f:
        a = json.load(f)
    with open(B_KEYS) as f:
        b = json.load(f)
    a_sk = unhexlify(a["sk"])
    b_pk = unhexlify(b["pk"])
    session_key = make_shared_key(a_sk, b_pk)
    nonce, ct = lock_message(session_key, msg, extra_data=b"A->B")
    env = {"from":"A","to":"B","nonce":nonce.hex(),"ciphertext":ct.hex()}
    open(outfile,"w").write(json.dumps(env))
    print(f"Wrote {outfile} (msg: {msg.decode()[:40]})")
    return session_key

def decrypt_with_key(sk_path, envelope_path="envelope.json"):
    with open(sk_path) as f:
        skj = json.load(f)
    with open(B_KEYS) as f:
        b = json.load(f)
    sk = unhexlify(skj["sk"])
    b_pk = unhexlify(b["pk"])
    env = json.load(open(envelope_path))
    nonce = unhexlify(env["nonce"]); ct = unhexlify(env["ciphertext"])
    session_key = make_shared_key(sk, b_pk)
    try:
        pt = unlock_message(session_key, nonce, ct, extra_data=b"A->B")
        print(f"Decrypted ({envelope_path}) with {sk_path}: {pt.decode()}")
    except Exception as e:
        print(f"Failed to decrypt {envelope_path} with {sk_path}: {repr(e)}")

if __name__ == "__main__":
    # Create two messages historically
    write_envelope(b"Message 1: first confidential message", outfile="env1.json")
    write_envelope(b"Message 2: second confidential message", outfile="env2.json")

    # Simulate attacker stealing A's private key
    shutil.copyfile(A_KEYS, "attacker_keys.json")
    print("Simulated key theft: attacker_keys.json created (copy of clientA_keys.json)")

    # Attacker tries to decrypt both historic envelopes
    decrypt_with_key("attacker_keys.json", "env1.json")
    decrypt_with_key("attacker_keys.json", "env2.json")

    # Clean up (optional)
    # os.remove("attacker_keys.json")
