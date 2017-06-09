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

    def test_whole_process(self):
        shares = shamir.shamir(4321, 7, 3, 4969)
        self.assertEqual(4321, shamir.reconstruct_secret(shares[1:4], 3, 4969))

if __name__ == '__main__':
    unittest.main()
