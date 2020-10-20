from sympy.discrete.transforms import ntt
from sympy.ntheory import isprime, primitive_root
import random


def find_prime(n):
    """Pick a prime number k*n+1 for some k."""
    for k in range(1, 100):
        p = k * n + 1
        if isprime(p):
            return p
    assert False, 'prime not found!!!1111one'


def naive_ntt(inp, P, omegas):
    """Simple NTT from Shunning."""
    N = len(inp)
    ret = [0] * N
    for i in range(N):
        for j in range(N):
            ret[i] = (ret[i] + inp[j] * omegas[(i * j) % N]) % P
    return ret


def main(n=2048):
    p = find_prime(n)

    a = [random.randint(0, 1000) for _ in range(n)]

    sympy_res = ntt(a, prime=p)

    # Generate an omega: g^k (mod p) for a generator of the field, g.
    g = primitive_root(p)
    k = (p - 1) // n
    omega = (g ** k) % p

    # Generate pre-computed omega array.
    omegas = [1]
    for i in range(n):
        omegas.append(omegas[i] * omega % p)
    for i in range(n):
        assert omegas[n - i] * omegas[i] % p == 1

    naive_res = naive_ntt(a, p, omegas)

    for i, (x, y) in enumerate(zip(sympy_res, naive_res)):
        assert x == y, 'difference at element {}'.format(i)
    print('ok!')


if __name__ == '__main__':
    main()
