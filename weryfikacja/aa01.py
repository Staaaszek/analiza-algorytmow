"""Numeryczna weryfikacja wyników z zestawu 1."""
import math
import random
from fractions import Fraction as F

# Zadanie 1: M(2^k) = 2 M(2^(k-1)) + 2^(k-1) + 2^k, M(1) = 0  =>  M(2^n) = 3 n 2^(n-1)
m = 0
for k in range(1, 40):
    m = 2 * m + 2 ** (k - 1) + 2**k
    assert m == 3 * k * 2 ** (k - 1)
print("ok  zad1")

# Zadanie 3: S(m) = T(3^m)/9^m spełnia S(m) = S(m-1) + 1/(m lg 3)
T1 = 1.0
for mm in range(1, 30):
    n = 3**mm
    t = T1
    for j in range(1, mm + 1):  # T(3^j) = 9 T(3^(j-1)) + 9^j / lg(3^j)
        t = 9 * t + 9**j / math.log2(3**j)
    hm = sum(1 / j for j in range(1, mm + 1))
    assert math.isclose(t, n**2 * (T1 + hm / math.log2(3)), rel_tol=1e-9)
print("ok  zad3")


# Zadanie 4: T(n) = c(q r + a q(q+1)/2) + q T(a) + T(r), n = q a + r, 0 < r <= a
def t4(n, a, c, base):
    return base(n) if n <= a else t4(n - a, a, c, base) + t4(a, a, c, base) + c * n


for a in range(1, 6):
    base = lambda x: 7 * x + 3  # dowolne wartości początkowe
    for n in range(1, 200):
        q, r = divmod(n, a)
        if r == 0:
            q, r = q - 1, a
        assert t4(n, a, 2, base) == 2 * (q * r + a * q * (q + 1) // 2) + q * base(a) + base(r)
print("ok  zad4")


# Zadanie 8: T(n) = H_{lg* n} - 1
def lgstar(x):
    k = 0
    while x > 1:
        x = math.log2(x)
        k += 1
    return k


def t8(n):
    return F(0) if n <= 2 else t8(math.ceil(math.log2(n))) + F(1, lgstar(n))


def Hn(n):
    return sum((F(1, k) for k in range(1, n + 1)), F(0))


for n in list(range(1, 3000)) + [65536, 65537, 2**100, 2**65536 + 1]:
    assert t8(n) == Hn(lgstar(n)) - 1 if n > 2 else t8(n) == 0, n
print("ok  zad8")


# Zadanie 10: dziel i zwyciężaj, z licznikiem porównań
def max_subarray(A, lo, hi, cnt):
    if lo == hi:
        return lo, hi, A[lo]
    mid = (lo + hi) // 2
    l = max_subarray(A, lo, mid, cnt)
    r = max_subarray(A, mid + 1, hi, cnt)
    # najlepszy sufiks lewej połowy
    s = best = A[mid]
    i = mid
    for k in range(mid - 1, lo - 1, -1):
        s += A[k]
        cnt[0] += 1
        if s > best:
            best, i = s, k
    left_best = best
    # najlepszy prefiks prawej połowy
    s = best = A[mid + 1]
    j = mid + 1
    for k in range(mid + 2, hi + 1):
        s += A[k]
        cnt[0] += 1
        if s > best:
            best, j = s, k
    cross = (i, j, left_best + best)
    res = l
    cnt[0] += 1
    if r[2] > res[2]:
        res = r
    cnt[0] += 1
    if cross[2] > res[2]:
        res = cross
    return res


random.seed(1)
for n in range(1, 120):
    for _ in range(20):
        A = [random.randint(-20, 20) for _ in range(n)]
        cnt = [0]
        i, j, s = max_subarray(A, 0, n - 1, cnt)
        brute = max(sum(A[x : y + 1]) for x in range(n) for y in range(x, n))
        assert s == brute == sum(A[i : j + 1])
        k = (n - 1).bit_length()
        assert cnt[0] == n * k + n - 2**k, (n, cnt[0])
print("ok  zad10")


# Master theorem, przypadek 2 dla k > -1, k = -1, k < -1:
# T(2^m) = 2 T(2^(m-1)) + 2^m * m^k  =>  T(2^m)/2^m = T(1) + sum_{j<=m} j^k
def master_ratio(m, k):
    t = 1.0
    for j in range(1, m + 1):
        t = 2 * t + 2**j * j**k
    return t / 2**m


for k, g in [(1, lambda m: m**2), (0.5, lambda m: m**1.5), (-1, lambda m: math.log(m)), (-2, lambda m: 1)]:
    r = [master_ratio(m, k) / g(m) for m in (200, 400, 800)]
    assert max(r) / min(r) < 1.3, (k, r)  # iloraz ustabilizowany => Theta(g)
print("ok  master k>-1, k=-1, k<-1")


# Akra-Bazzi: wykładniki p z zadania 7 i sprawdzenie Theta(n) wprost
def solve_p(bs):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if sum(b**mid for b in bs) > 1 else (lo, mid)
    return lo


assert abs(solve_p([0.2, 0.7]) - 0.8398) < 1e-3
assert abs(solve_p([0.2, 0.75]) - 0.9114) < 1e-3
for b1, b2 in [(5, 0.7), (5, 0.75)]:
    T = [1.0] * 50
    for n in range(50, 200001):
        T.append(T[math.ceil(n / b1)] + T[math.ceil(b2 * n)] + n)
    # T(n)/n ograniczone przez ~1/(1 - suma współczynników) => T = Theta(n)
    bound = 1 / (1 - (1 / b1 + b2)) + 1
    assert max(T[n] / n for n in range(50, len(T))) < bound
print("ok  akra-bazzi (zad7)")
