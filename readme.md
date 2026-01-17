
## Project: Protocol Implementation (COMP5005)

This repository contains small Python demos that implement and test cryptographic protocol properties:
- Key generation
- Message encryption + decryption
- Wrong-key decryption failure
- Forward secrecy behaviour across sessions

### Folder structure
- `src/` – implementation and demo scripts
- `evidence/terminal_logs/` – captured terminal outputs for each run
- `evidence/artefacts/` – generated JSON artefacts (demo keys, envelopes)

### How to run (Windows / VS Code)
-In powershell, activate script by running
python -m venv .venv
.\.venv\Scripts\Activate.ps1
-pip install -r requirements.txt
-cd src
-python keygen_demo.py
-python encrypt_demo.py
-python decrypt_demo.py
-python wrong_key_decrypt.py
-python forward_secrecy_demo.py

###Scripts
utils.py — It does the math: key generation, shared secret derivation (X25519 + HKDF), encryption/decryption (ChaCha20-Poly1305). this script basically defines all the functions to be used in other scripts

keygen_demo.py — both “clients” (A and B) make their public/private keys here.
It saves them as JSON because .

encrypt_send_demo.py — pretends to be Client A sending a secret to B.
It uses A’s private key and B’s public key to get a shared session key, encrypts the message into sort of an envelope known as That’s the ciphertext.

decrypt_receive_demo.py — pretends to be Client B receiving the message.
It does the reverse math using B’s private key and A’s public key, recovers the same shared session key, decrypts, and prints the original message.


run keygen_demo first to generate the keys for A and B
then run encrypt_demo to encrypt and send the message
finally, run decrypt_demo to receive and decrypt the message
run wrong_key_decrypt to show what happens when an attacker tries to decrypt using another key
run forward_secrecy_demo to show what happens when an attacker gains a previous key and tries to decrypt