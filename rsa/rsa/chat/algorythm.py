from Crypto.Util.number import getPrime
from random import choice, randint


class RSA:

    FERMA_NUMBERS = [3, 5, 17, 257, 65537]

    def generate_keys(self):
        P = getPrime(30)
        Q = getPrime(30)

        N = P * Q
        E_func = (P - 1) * (Q - 1)

        E = choice(self.FERMA_NUMBERS)

        while E >= E_func:
            E = choice(self.FERMA_NUMBERS)

        D = self._multiplicative_inverse(E, E_func)

        return E, N, D

    def decrypt(self, char: str, d: int, n: int) -> str:
        number = ord(char)

        result = pow(number, d) % n

        return oct(result)

    def encrypt(self, char: str, e: int, n: int) -> int:
        number = ord(char)

        result = pow(number, e) % n

        return result

    def _multiplicative_inverse(self, a, b):
        '''
        An implementation of extended Euclidean algorithm.
        Returns integer x, y and gcd(a, b) for Bezout equation:
            ax + by = gcd(a, b).
            E*(-D) + E_func*k = 1
        '''
        x, xx, y, yy = 1, 0, 0, 1
        while b:
            q = a // b
            a, b = b, a % b
            x, xx = xx, x - xx * q
            y, yy = yy, y - yy * q
        # return (x, y, a)
        return -x
