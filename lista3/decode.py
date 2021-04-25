def decode(c, private_key):
    W = private_key[0]
    q = private_key[1]
    r = private_key[2]

    r_reverse = pow(r, -1, q)
    reversed_c = (c * r_reverse) % q
    W.reverse()
    message = 0
    for w in W:
        message <<= 1
        if reversed_c >= w:
            message += 1
            reversed_c -= w
    return message


if __name__ == "__main__":
    print(decode(74, ([1, 3, 6, 19], 42, 19)))