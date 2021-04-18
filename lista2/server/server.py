from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import os

n = 16
N_BYTES = n//8
KEY_MAP_FILENAME = os.path.join('../output', 'key_map.txt')
ENCODED_KEYS_FILENAME = os.path.join('../output', 'puzzle.encrypted')
ID_FILENAME = os.path.join('../output', 'id.txt')
BREAKABLE_KEY_LENGTH = 16
SECURE_KEY_LENGTH = 32
KEY_ID_LENGTH = 16


def generate_puzzles():
    with open(KEY_MAP_FILENAME, 'wb') as key_map_file:
        with open(ENCODED_KEYS_FILENAME, 'wb') as puzzle_file:
            for i in range(2 ** n):
                puzzle_key = b'\xff' * (BREAKABLE_KEY_LENGTH - N_BYTES) + get_random_bytes(N_BYTES)

                cipher = AES.new(puzzle_key, AES.MODE_GCM)

                puzzle_file.write(cipher.nonce)
                encrypted_key = get_random_bytes(SECURE_KEY_LENGTH)
                key_id = hashlib.shake_128(encrypted_key).digest(KEY_ID_LENGTH)
                data = b'msg:' + key_id + encrypted_key
                key_map_file.write(key_id)
                key_map_file.write(encrypted_key)

                encrypted_data = cipher.encrypt(data)
                puzzle_file.write(encrypted_data)


def get_key_from_ids():
    with open(ID_FILENAME, 'rb') as id_file:
        key_id = id_file.read(KEY_ID_LENGTH)
    print(key_id)
    with open(KEY_MAP_FILENAME, 'rb') as key_map_file:
        while line := key_map_file.read(KEY_ID_LENGTH + SECURE_KEY_LENGTH):
            if line[0:KEY_ID_LENGTH] == key_id:
                print("id = ", line[0:KEY_ID_LENGTH])
                print("key = ", line[KEY_ID_LENGTH:])
                break


if __name__ == "__main__":
    #generate_puzzles()
    get_key_from_ids()
