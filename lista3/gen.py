import random


def generate(n):
    W = []
    sum_of_W = 0
    for i in range(0, n):
        next_number = random.randint(sum_of_W + 1, 2 * (sum_of_W + 1))
        W.append(next_number)
        sum_of_W += next_number
    print(W)
    q = random.randint(sum_of_W + 1, 2 * sum_of_W + 1)

    r = random.randint(2 ** n, 2 ** (n + 1))
    while not is_coprime(q, r):
        r = random.randint(2 ** n, 2 ** (n + 1))

    B = []
    for w in W:
        B.append((r * w) % q)

    return B, (W, q, r)


def gcd(p, q):
    while q != 0:
        p, q = q, p % q
    return p


def is_coprime(x, y):
    return gcd(x, y) == 1


if __name__ == "__main__":
    print(generate(4))
