import unittest
import shamir

class ShamirTest(unittest.TestCase):

    def test_generate_coefficients(self):
        coef = shamir._generate_coefficients(4321, 5, 4969)
        self.assertEqual(5, len(coef))
        self.assertEqual(4321, coef[0])
        for i in coef:
            self.assertLess(i, 4969)

    def test_generate_shares(self):
        #import pdb; pdb.set_trace()
        shares = shamir._generate_shares([4321, 214, 173], 7, 4969)
        self.assertEqual(7, len(shares))
        result = [(1, 4708), (2, 472), (3, 1551), (4, 2976), (5, 4747), (6, 1895), (7, 4358)]
        self.assertListEqual(result, shares)

    def test_inverse(self):
        prime = 2**19-1
        a = 12345
        self.assertEqual(1, a*shamir.inverse(a, prime) % prime)

    def test_whole_process(self):
        secret = 123456
        n = 120
        t = 58
        prime = 2**19-1
        #secret = 32
        #n = 5
        #t = 3
        #prime = 53
        #import pdb; pdb.set_trace()
        shares = shamir.shamir(secret, n, t, prime)
        self.assertEqual(secret, shamir.reconstruct_secret(shares[0:t], t, prime))

if __name__ == '__main__':
    unittest.main()
