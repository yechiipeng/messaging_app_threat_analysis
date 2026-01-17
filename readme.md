# Messaging Application Threat Analysis & Cryptographic Protocol Demonstration

This repository contains a practical security analysis and cryptographic protocol demonstration for a modern messaging application architecture. The project was developed as part of my university module named COMP5005 and focuses on how confidentiality, authentication, and forward secrecy are implemented and verified in practice.

The work demonstrates both correct cryptographic behaviour and failure cases, supported by captured execution evidence to ensure reproducibility and auditability.

## System Context

The target system follows a standard messaging architecture consisting of:

- Client: Messaging application running on a user device
- Server: Backend responsible for routing messages and managing sessions
- Database: Stores message metadata and system state

This project focuses on protocol behaviour at the client side and cryptographic properties rather than UI or network transport.


## Security Properties Demonstrated

The implementation demonstrates the following properties:

- Confidentiality: Messages are encrypted before transmission
- Authentication: Only holders of the correct private keys can decrypt messages
- Forward Secrecy: Compromise of long-term keys should not expose past messages
- Failure Handling: Incorrect keys cannot decrypt protected content


## Repository Structure
├── src/
│ ├── keygen_demo.py
│ ├── encrypt_demo.py
│ ├── decrypt_demo.py
│ ├── wrong_key_decrypt.py
│ ├── forward_secrecy_demo.py
│ └── utils.py
│
├── evidence/
│ └── terminal_logs/
│ ├── 01_keygen.txt
│ ├── 02_encrypt.txt
│ ├── 03_decrypt.txt
│ ├── 04_wrong_key.txt
│ └── 05_forward_secrecy.txt
│
├── requirements.txt
└── README.md


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

######Scripts
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



#Key Security Observations
-Cryptographic security collapses if private keys are compromised
-Unfortunately in this case, forward secrecy wasnt applied. The demonstration shows that attackers are able to achieve retrospective message disclosure with long term keys
-Incorrect key usage reliably results in decryption failure
-Generated keys are intentionally excluded from the repository via .gitignore.

##Academic Context
This project aligns with:
-Secure protocol design principles
-Evidence-first security analysis
-Modern messaging security models used in real-world applications
-It demonstrates practical understanding beyond theoretical descriptions.

#Author
Tojehova Onyinyechukwu Ajero
Cybersecurity Graduate
Focus: SOC Operations, Security Architecture, Applied Cryptography
