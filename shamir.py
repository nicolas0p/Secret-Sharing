import random

def _generate_coefficients(secret, threshold, prime):
    coefficients = [secret]
    for i in range(1, threshold):
        coefficients.append(random.randrange(prime))
    return coefficients

"""Calculates f(x) for a polynomial with coefficients and x mod prime
@param coefficients The polynomial coefficients
@param x point for which the polynomial should be calculated
@returns f(x) = coef[0] + coef[1]*x + coef[2]*x^2 + ... + coef[n]*x^n mod prime"""
def _calculate_polynomial(coefficients, x, prime):
    var = 1
    result = 0
    for coef in coefficients:
        result = (result + coef * var) % prime
        var = var * x % prime
    return result % prime

def _generate_shares(coefficients, quantity, prime):
    shares = []
    for i in range(1, quantity + 1):
        shares.append((i, _calculate_polynomial(coefficients, i, prime)))
    return shares

def shamir(secret, members_quantity, threshold, prime):
    coefficients = _generate_coefficients(secret, threshold, prime) #coefficients will contain 'threshold' items. coef[0] = secret
    shares = _generate_shares(coefficients, members_quantity, prime);
    return shares

"""@returns a^-1 mod n"""
def inverse(a, n):
    t = 0; newt = 1
    r = n; newr = a % n
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        return False #a is not invertible mod n
    if t < 0:
        t += n
    return t

def reconstruct_secret(shares, threshold, prime):
    if len(shares) < threshold:
        return "At least t shares are needed to calculate the secret"

    result = 0
    for i in range(threshold):
        partial = shares[i][1]
        for m in range(threshold):
            if m == i:
                continue
            partial *= (shares[m][0] * inverse(shares[m][0] - shares[i][0], prime) % prime)
        result += partial % prime
    return result % prime

if __name__ == "__main__":
    secret = int(input("Type in the secret:"))
    n = int(input("Type in the n:"))
    t = int(input("Type in the t:"))
    prime = int(input("Type in the prime:"))
    shares = shamir(secret, n, t, prime)
    result = reconstruct_secret(shares[0:t], t, prime)
    print("The reconstructed secret is: " + str(result))
