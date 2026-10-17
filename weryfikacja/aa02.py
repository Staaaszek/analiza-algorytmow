"""Weryfikacja wyników z zestawu 2 (dokładnie: ułamki, pełne przeglądy)."""
import itertools
import math
from fractions import Fraction as F


def H(n):
    return sum((F(1, k) for k in range(1, n + 1)), F(0))


# Zadanie 1: N = liczba zer przed pierwszą jedynką, zwracamy N mod 2.
# P(0) = sum_{m nieparz.} p^m q = p/(1+p);  E[liczba wywołań] = 1/(1-p).
for p in [F(1, 3), F(1, 2), F(7, 10), F(99, 100)]:
    q = 1 - p
    # łańcuch: stan "parzysto zer" (start) / "nieparzysto zer"
    # P0 = prawdopodobieństwo wyniku 0 startując z parzystego: P0 = p*(q*1 + p*P0)
    P0 = p * q / (1 - p * p)
    assert P0 == p / (1 + p)
    # E: E_even = 1 + p E_odd,  E_odd = 1 + p E_even
    E = (1 + p) / (1 - p * p)
    assert E == 1 / (1 - p)
    # niezależnie: suma szeregu (obcięta) zgadza się z wzorem
    approx = sum(float(p) ** m * float(q) for m in range(1, 4000, 2))
    assert abs(approx - float(p / (1 + p))) < 1e-9
print("ok  zad1")


# Zadanie 2: P(dokładnie 2 zatrudnienia) = H_{n-1}/n
def hires(perm):
    best, c = -1, 0
    for x in perm:
        if x > best:
            best, c = x, c + 1
    return c


for n in range(1, 9):
    perms = list(itertools.permutations(range(n)))
    cnt = sum(1 for pm in perms if hires(pm) == 2)
    assert F(cnt, len(perms)) == (H(n - 1) / n if n > 1 else 0), n
print("ok  zad2")

# Zadanie 3: E[silne inwersje] = (n-k)(n-k-1)/4 dla k <= n-1, 0 dla k >= n-1
for n in range(1, 8):
    perms = list(itertools.permutations(range(1, n + 1)))
    for k in range(1, n + 3):
        tot = sum(
            sum(1 for i in range(n) for j in range(i + 1, n) if pm[i] > pm[j] + k)
            for pm in perms
        )
        expected = F((n - k) * (n - k - 1), 4) if k <= n - 1 else 0
        assert F(tot, len(perms)) == expected, (n, k)
print("ok  zad3")

# Zadanie 4: E[różne] = N(1 - (1-1/N)^n); dla N = n^3: n - 1/(2n) + 1/(2n^2) + O(n^-3)
for N in range(1, 6):
    for n in range(1, 5):
        tot = sum(len(set(t)) for t in itertools.product(range(N), repeat=n))
        assert F(tot, N**n) == N * (1 - (1 - F(1, N)) ** n), (N, n)
for n in [10, 20, 40, 80]:
    N = n**3
    E = N * (1 - (1 - F(1, N)) ** n)
    err = E - (n - F(1, 2 * n) + F(1, 2 * n * n))
    assert 0 < err * n**3 < F(1, 6) + F(1, 10), (n, float(err * n**3))
print("ok  zad4")


# Zadanie 5: E[X] = sum_{k=0}^{b} b^(k)/b^k  (X = numer rzutu z pierwszą kolizją)
def EX(b):
    s, t = F(0), F(1)
    for k in range(0, b + 1):
        s += t
        t *= F(b - k, b)
    return s


for b in range(1, 6):
    # dokładnie: przegląd wszystkich ciągów b+1 rzutów
    tot = F(0)
    for seq in itertools.product(range(b), repeat=b + 1):
        seen = set()
        for idx, u in enumerate(seq, 1):
            if u in seen:
                tot += idx
                break
            seen.add(u)
    assert tot / b ** (b + 1) == EX(b), b
for b in [100, 365, 1000, 10000]:
    e = float(EX(b)) if b <= 1000 else None
    if e is None:
        s, t = 0.0, 1.0
        for k in range(b + 1):
            s += t
            t *= (b - k) / b
        e = s
    approx = math.sqrt(math.pi * b / 2) + 2 / 3
    assert abs(e - approx) < 0.2 / math.sqrt(b), (b, e, approx)
assert abs(float(EX(365)) - 24.6166) < 1e-3
print("ok  zad5")

# Zadanie 6: najmniejsze n z C(n,3)/365^2 >= 1
n = 1
while math.comb(n, 3) < 365**2:
    n += 1
assert n == 94
print("ok  zad6")


# Zadania 7-9: pełny przegląd losowań
def is_ncycle(pm):
    n, x, c = len(pm), 0, 0
    while True:
        x, c = pm[x], c + 1
        if x == 0:
            return c == n


def dist(n, algo):
    from collections import Counter

    out = Counter()
    for choices, prob in algo(n):
        out[choices] += prob
    return out


def first(n):
    for ch in itertools.product(*[range(i + 1, n) for i in range(n - 1)]):
        A = list(range(n))
        for i, j in enumerate(ch):
            A[i], A[j] = A[j], A[i]
        yield tuple(A), F(1, math.factorial(n - 1))


def second(n):
    for ch in itertools.product(range(n), repeat=n):
        A = list(range(n))
        for i, j in enumerate(ch):
            A[i], A[j] = A[j], A[i]
        yield tuple(A), F(1, n**n)


def third(n):
    for off in range(1, n + 1):
        B = [None] * n
        for i in range(1, n + 1):
            d = i + off
            if d > n:
                d -= n
            B[d - 1] = i - 1
        yield tuple(B), F(1, n)


for n in range(1, 8):
    d = dist(n, first)
    assert len(d) == math.factorial(n - 1)
    assert all(is_ncycle(pm) for pm in d) and len(set(d.values())) == 1
print("ok  zad7")

for n in range(1, 7):
    d = dist(n, second)
    assert len(d) == math.factorial(n)
    assert (len(set(d.values())) == 1) == (n <= 2), n
d3 = dist(3, second)
assert sorted(d3.values()) == [F(4, 27)] * 3 + [F(5, 27)] * 3
print("ok  zad8")

for n in range(1, 8):
    d = dist(n, third)
    rot = {tuple((i - s) % n for i in range(n)) for s in range(n)}
    assert set(d) == rot and len(d) == n and set(d.values()) == {F(1, n)}
print("ok  zad9")
