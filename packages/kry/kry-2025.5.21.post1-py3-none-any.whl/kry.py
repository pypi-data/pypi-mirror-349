"""kry.py - Simple cryptography library

pip install kry
"""

__version__ = "2025.5.21-rev1"
__url__ = "https://github.com/krylib/kry"
__license__ = "Unlicense OR CC0-1.0" # released to public domain

import secrets

def divides(a, b):
    """Return True if a divides b"""
    return b % a == 0

def is_miller_rabin_probable_prime(w):
    """Return True if w is a miller rabin probable prime
    
    Reference: FIPS 186-5 B.3 and B.3.1
    """
    
    # we choose to perform optional trial division as noted in FIPS 186-5 B.3
    #fixme trial division
    ...

    #fixme iterations
    iterations = 4

    # 1.
    a = 0
    while divides(2**a, w - 1):
        a += 1 # divisible, let's check the next
    a -= 1 # not divisble anymore, use the previous one

    # 2.
    m = (w - 1) // 2**a

    # 3.
    wlen = w.bit_length()

    # 4.
    for i in range(iterations):
        while True:
            # 4.1
            b = secrets.randbits(wlen)

            # 4.2
            if b <= 1 or b >= w - 1:
                continue # go to 4.1
            else:
                break # go to 4.3

        # 4.3
        z = pow(b, m, w)

        # 4.4
        if z == 1 or z == w - 1:
            # 4.7
            continue # go to 4.

        # 4.5
        goto4_7 = False
        for j in range(a-1):
            # 4.5.1
            z = pow(z, 2, w)

            # 4.5.2
            if z == w - 1:
                goto4_7 = True
                break

            # 4.5.3
            if z == 1:
                break # go to 4.6

        if goto4_7:
            # 4.7
            continue

        # 4.6
        return False # composite

    # 5.
    return True # probably prime
