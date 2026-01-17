# keygen_demo.py
from utils import create_keys, key_to_bytes
import json

def save(name, sk, pk):
    data = {
        "sk": key_to_bytes(sk).hex(),
        "pk": key_to_bytes(pk).hex()
    }
    open(f"{name}_keys.json","w").write(json.dumps(data))

if __name__ == "__main__":
    a_sk, a_pk = create_keys()
    b_sk, b_pk = create_keys()
    save("clientA", a_sk, a_pk)
    save("clientB", b_sk, b_pk)
    print("Saved clientA_keys.json and clientB_keys.json")
