#this is a demo of communication between sender A and receiver B
utils.py — It does the math: key generation, shared secret derivation (X25519 + HKDF), encryption/decryption (ChaCha20-Poly1305). this script basically defines all the functions to be used in other scripts

keygen_demo.py — both “clients” (A and B) make their public/private keys here.
It saves them as JSON because .

encrypt_send_demo.py — pretends to be Client A sending a secret to B.
It uses A’s private key and B’s public key to get a shared session key, encrypts the message into sort of an envelope known as That’s the ciphertext.

decrypt_receive_demo.py — pretends to be Client B receiving the message.
It does the reverse math using B’s private key and A’s public key, recovers the same shared session key, decrypts, and prints the original message.

to run simply type in terminal "python *filename*
run keygen_demo first to generate the keys for A and B
then run encrypt_demo to encrypt and send the message
finally, run decrypt_demo to receive and decrypt the message