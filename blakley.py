import sys
sys.path.insert(0, './Galois')
from galois import GF
from coding import Matrix

import random

"""
@member _secret_point contains the secret point. _secret_point[0] is the secret
@member _prime the prime used to generate Zp
@member _threshold minimum amount of shares needed to calculate the secret
it also defines the amount of dimensions used in the secret point and the vectors
"""
class Blakley:

    def __init__(self, secret, t, prime):
        if t < 2:
            raise "t must be greater than 2"
        if secret >= prime:
            raise "secret must be less than prime"

        self._secret_point = [secret]
        for i in range(t-1):
            self._secret_point.append(random.randrange(prime))
        self._threshold = t
        self._prime = prime

    def generate_share(self):
        t = self._threshold
        prime = self._prime
        constant = self._secret_point[-1]
        vector = []
        for i in range(t - 1):
            coef = random.randrange(prime)
            vector.append(coef)
            constant -= (coef * self._secret_point[i]) % prime
        vector.append(constant % prime)
        return vector

    def calculate_secret(self, shares):
        if len(shares) < self._threshold:
            raise "You need at least t shares to calculate the secret"
        t = self._threshold
        prime = self._prime
        a = []
        b = [[]]
        for i in range(t):
            a.append(shares[i][0:t - 1])
            a[i].append(-1)
            b[0].append(-shares[i][-1])
        A = Matrix(data = a).to_Zmod(prime)
        B = Matrix(data = b).transpose().to_Zmod(prime)
        aug = A.join_with(B)
        solution = aug.get_reduced_echelon().submatrix(0, t, t, 1)
        return int(solution.get(0,0))

if __name__ == "__main__":
    secret = int(input("Type in the secret:"))
    t = int(input("Type in the t:"))
    prime = int(input("Type in the prime:"))
    bl = Blakley(secret, t, prime)
    shares = []
    print("Initial t shares(more can be generated):")
    for i in range(t):
        generated = bl.generate_share()
        shares.append(generated)
        print(generated)
    result = bl.calculate_secret(shares)
    print("The reconstructed secret is: " + str(result))
