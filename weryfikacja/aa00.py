"""Numeryczna weryfikacja wzorów zwartych z zestawu 0 (dokładnie, na ułamkach)."""
import math
from fractions import Fraction as F


def H(n):
    return sum((F(1, k) for k in range(1, n + 1)), F(0))


def ff(n, m):
    """Potęga krocząca w dół n^(m) = n(n-1)...(n-m+1)."""
    r = 1
    for i in range(m):
        r *= n - i
    return r


def check(name, rec, closed, ns):
    for n in ns:
        assert rec[n] == closed(n), (name, n, rec[n], closed(n))
    print(f"ok  {name}")


N = 60

# Zadanie 5: H_n nie jest całkowita dla n > 1
for n in range(2, 300):
    assert H(n).denominator != 1
print("ok  zad5")

# Zadanie 6: ln n < H_n < ln n + 1
for n in range(2, 2000):
    h = float(H(n)) if n < 200 else sum(1 / k for k in range(1, n + 1))
    assert math.log(n) < h < math.log(n) + 1
print("ok  zad6")

# Zadanie 7
a = {0: F(1)}
for n in range(1, N):
    a[n] = F(n, n + 2) * a[n - 1]
check("zad7a", a, lambda n: F(2, (n + 1) * (n + 2)), range(N))

a = {0: F(1)}
for n in range(1, N):
    a[n] = a[n - 1] + (-1) ** n
check("zad7b", a, lambda n: F(1 + (-1) ** n, 2), range(N))

a = {1: F(1)}
for n in range(2, N):
    a[n] = F(1, n) * ((n - 2) * a[n - 1] + 2)
check("zad7c", a, lambda n: 1, range(1, N))

a = {1: 1}
for n in range(2, N):
    a[n] = 2 * a[n - 1] + 1
check("zad7d", a, lambda n: 2**n - 1, range(1, N))

a = {0: F(0)}
for n in range(1, N):
    a[n] = F(n + 1, n) * a[n - 1] + 2
check("zad7e", a, lambda n: 2 * (n + 1) * (H(n + 1) - 1), range(N))

a = {n: F(0) for n in range(5)}
for n in range(5, N):
    a[n] = F(n - 4, n) * a[n - 1] + 12 * H(n)
check(
    "zad7f",
    a,
    lambda n: F(12, 5) * (n + 1) * H(n) - F(12 * (n - 4), 25) - F(600, ff(n, 4)),
    range(4, N),
)

# lemat do 7f: sum_{0<=k<n} k^(m) H_k = n^(m+1)/(m+1) * (H_n - 1/(m+1))
for m in range(0, 6):
    for n in range(0, 30):
        lhs = sum((ff(k, m) * H(k) for k in range(n)), F(0))
        assert lhs == F(ff(n, m + 1), m + 1) * (H(n) - F(1, m + 1))
print("ok  lemat 7f")


# Zadanie 8: f(n) = 1 + ceil(lg lg n) dla n > 2 (argument rzeczywisty)
def f8(x):
    return 1 if x <= 2 else 1 + f8(math.sqrt(x))


for n in list(range(3, 5000)) + [2**16, 2**16 + 1, 2**32]:
    lglg = math.log2(math.log2(n))
    expected = 1 + math.ceil(lglg - 1e-12)
    assert f8(n) == expected, (n, f8(n), expected)
print("ok  zad8")

# Zadanie 9
C = {1: 0}
for n in range(2, 5000):
    C[n] = C[n // 2] + C[(n + 1) // 2] + n - 1
for n in range(1, 5000):
    k = (n - 1).bit_length()  # = ceil(lg n)
    assert C[n] == n * k + 1 - 2**k, n
print("ok  zad9")
