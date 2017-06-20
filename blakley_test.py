import unittest
import blakley

"""
vector contains a, b, c... such that z = ax + by + cw + ... is the vector equation
z is point[-1]
"""
def point_in_vector(point, vector, prime):
    result = 0
    if len(point) != len(vector):
        return False
    for i in range(len(point)-1):
        result += (point[i] * vector[i]) % prime
    result += vector[-1] #the last member contains the constant
    result = result % prime
    return result == point[-1]

class BlakleyTest(unittest.TestCase):

    def test_generate_share(self):
        secret = 4321
        t = 5
        prime = 4969
        bl = blakley.Blakley(secret, t, prime)
        vector = bl.generate_share()
        self.assertTrue(point_in_vector(bl._secret_point, vector, bl._prime))

    def test_point_in_vector(self):
        corret = [42, 29, 57]
        wrong = [42, 29, 56]
        vector = [57, 12, 16]
        prime = 73
        self.assertTrue(point_in_vector(corret, vector, prime))
        self.assertFalse(point_in_vector(wrong, vector, prime))

    def test_calculate_secret(self):
        secret = 0 #we do not know the secret
        t = 3
        prime = 73
        bl = blakley.Blakley(secret, t, prime)
        shares = [[4,19,68], [52,27,10], [36,65,18], [57, 12, 16], [34, 19, 49]]
        calculated = bl.calculate_secret(shares)
        self.assertEqual(42, calculated)

    def test_generate_shares_and_calculate_secret(self):
        secret = 4321
        t = 42
        prime = 4969
        bl = blakley.Blakley(secret, t, prime)
        shares = []
        for i in range(t):
            shares.append(bl.generate_share())
        calculated = bl.calculate_secret(shares)
        self.assertEqual(secret, calculated)

if __name__ == '__main__':
    unittest.main()
