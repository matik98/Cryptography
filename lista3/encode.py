def encode(m, B):
    encoded_message = 0
    for b in B:
        if m % 2 == 1:
            encoded_message += b
        m >>= 1
    return encoded_message


if __name__ == "__main__":
    print(encode(13, [19, 15, 30, 25]))
