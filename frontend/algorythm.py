from Crypto.Util.number import getPrime
from random import choice, randint


class RSA:

    FERMA_NUMBERS = [5, 17, 257, 65537]

    def generate_keys(self):
        P = getPrime(9)
        Q = getPrime(9)

        N = P * Q
        E_func = (P - 1) * (Q - 1)

        E = choice(self.FERMA_NUMBERS)

        while E >= E_func:
            E = choice(self.FERMA_NUMBERS)

        D = self._multiplicative_inverse(E, E_func)

        return E, N, D

    def decrypt(self, number: int, d: int, n: int) -> str:

        result = pow(number, abs(d)) % n

        return chr(result)

    def encrypt(self, char: str, e: int, n: int) -> str:
        number = ord(char)

        result = pow(number, e) % n

        return str(result) + ' '

    def _egcd(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, x, y = self._egcd(b % a, a)
            return g, y - (b // a) * x, x

    def _multiplicative_inverse(self, b, n):
        '''
        # x = mulinv(b) mod n, (x * b) % n == 1
        '''
        g, x, _ = self._egcd(b, n)

        if g == 1:
            return x % n

    def decrypt_str(self, string, d, n):
        result = ''
        print(string.split())
        for number in string.split():
            result += self.decrypt(int(number), d, n)
        return result

    def encrypt_str(self, string, e, n):
        result = list()
        for letter in string:
            result.append(self.encrypt(letter, e, n))
        return ' '.join(result)
