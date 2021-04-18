import os
import random
from Crypto.Cipher import AES

NONCE_LENGTH = 16
n = 16
N_BYTES = n//8
BREAKABLE_KEY_LENGTH = 16
SECURE_KEY_LENGTH = 32
ENCRYPTED_DATA_LENGTH = 52
KEY_ID_LENGTH = 16
ENCODED_KEYS_FILENAME = os.path.join('../output', 'puzzle.encrypted')
ENCODED_MESSAGE_FILE = os.path.join('../output', 'message.encrypted')
MESSAGE_FILE = os.path.join('../output', 'message.txt')
DECODED_MESSAGE_FILE = os.path.join('../output', 'decoded_message.txt')
BUFFER_SIZE = 1024 * 1024


def decode(decode_key, encoded_data, nonce):
    cipher = AES.new(decode_key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt(encoded_data)  # Decrypt the data


def encode_file(key):
    with open(MESSAGE_FILE, 'rb') as message_file:
        with open(ENCODED_MESSAGE_FILE, 'wb') as encoded_file:
            cipher = AES.new(key, AES.MODE_GCM)
            encoded_file.write(cipher.nonce)
            while data := message_file.read(BUFFER_SIZE):
                encrypted_data = cipher.encrypt(data)
                encoded_file.write(encrypted_data)


def decode_file(key):
    with open(ENCODED_MESSAGE_FILE, 'rb') as encoded_file:
        with open(DECODED_MESSAGE_FILE, 'wb') as decoded_file:
            nonce = encoded_file.read(NONCE_LENGTH)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

            while data := encoded_file.read(BUFFER_SIZE):
                decrypted_data = cipher.decrypt(data)
                decoded_file.write(decrypted_data)


def solve_puzzles():
    message_index = random.randint(0, 2 ** n - 1)
    with open(ENCODED_KEYS_FILENAME, 'rb') as puzzle_file:

        # Skip unwanted data
        for i in range(message_index):
            puzzle_file.read(NONCE_LENGTH + ENCRYPTED_DATA_LENGTH)

        # Read nonce and create cipher
        nonce = puzzle_file.read(NONCE_LENGTH)  # The nonce is 16 bytes long

        data = puzzle_file.read(ENCRYPTED_DATA_LENGTH)
        for i in range(2 ** n):
            key = b'\xff' * (BREAKABLE_KEY_LENGTH - N_BYTES) + i.to_bytes(N_BYTES, 'big')
            decrypted_data = decode(key, data, nonce)
            if decrypted_data[0:4] == b'msg:':
                print("done")
                break

        print("msg:", decrypted_data[0:4])
        print("id:", decrypted_data[4:20])
        print("key:", decrypted_data[20:52])

        id_filename = os.path.join('../output', 'id.txt')
        with open(id_filename, 'wb') as id_file:
            id_file.write(decrypted_data[4:20])


if __name__ == "__main__":
    key = b'\xee\x9c~P?\xe3N\xb0\x00\x8be\xbdT\xbd\x9fu\x04\xf0UUq\x8d\xda>Q\xe8\xecv5\xcd\xf5\x00'
    encode_file(key)
    decode_file(key)
