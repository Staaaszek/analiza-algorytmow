"""Weryfikacja wyników z zestawu 3 (funkcje tworzące; ułamki, szeregi, brute force)."""
import itertools
import math
from fractions import Fraction as F

N = 30  # ile współczynników szeregów porównujemy


def H(n):
    return sum((F(1, k) for k in range(1, n + 1)), F(0))


def mul(a, b, n=N):
    """Iloczyn szeregów formalnych (listy współczynników) obcięty do n wyrazów."""
    out = [F(0)] * n
    for i, x in enumerate(a[:n]):
        if x:
            for j, y in enumerate(b[: n - i]):
                out[i + j] += x * y
    return out


geo = [F(1)] * N  # 1/(1-x)
ln = [F(0)] + [F(1, n) for n in range(1, N)]  # zadanie 1: sum x^n / n

# Zadanie 1: F(x) = ln(1/(1-x)); pochodna: sum x^(n-1) = 1/(1-x); wartość w punkcie
for x in [0.1, 0.5, 0.9]:
    s = sum(x**n / n for n in range(1, 2000))
    assert abs(s - math.log(1 / (1 - x))) < 1e-12, x
# (1-x) * F'(x) = 1 jako szereg
d = [n * ln[n] for n in range(1, N)]  # współczynniki F'(x)
one_minus_x = [F(1), F(-1)]
assert mul(d, one_minus_x, N - 1) == [F(1)] + [F(0)] * (N - 2)
print("ok  zad1")

# Zadanie 2: H(x) = 1/(1-x) * ln(1/(1-x)) ma współczynniki H_n,
# a (1/2) ln^2(1/(1-x)) ma współczynniki H_{n-1}/n
Hx = mul(geo, ln)
assert Hx == [H(n) for n in range(N)]
half_sq = [c / 2 for c in mul(ln, ln)]
assert half_sq == [F(0)] + [H(n - 1) / n for n in range(1, N)]
# całkowanie: współczynnik przy x^n w całce z H(x) to H_{n-1}/n
assert [F(0)] + [Hx[n - 1] / n for n in range(1, N)] == half_sq


# ... i to jest prawdopodobieństwo z zadania 2 zestawu 2
def hires(perm):
    best, c = -1, 0
    for x in perm:
        if x > best:
            best, c = x, c + 1
    return c


for n in range(2, 8):
    perms = list(itertools.permutations(range(n)))
    cnt = sum(1 for pm in perms if hires(pm) == 2)
    assert F(cnt, len(perms)) == half_sq[n], n
print("ok  zad2")

# Zadanie 3: F(x,y) = xy/(1-x-xy)^2, współczynnik przy x^n y^m = m C(n,m)
M = 14
# 1/(1-u)^2 = sum (k+1) u^k, u = x(1+y);  F = x y sum_k (k+1) x^k (1+y)^k
coef = {}
for k in range(M):
    for j in range(k + 1):
        key = (k + 1, j + 1)  # x^(k+1) y^(j+1)
        coef[key] = coef.get(key, 0) + (k + 1) * math.comb(k, j)
for n in range(M):
    for m in range(n + 1):
        assert coef.get((n, m), 0) == m * math.comb(n, m), (n, m)
print("ok  zad3")


# Zadanie 4: sum_k n/(n-k) C(n-k,k) = L_n  (n >= 1)
def lucas(n):
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a


for n in range(1, 60):
    s = sum(F(n, n - k) * math.comb(n - k, k) for k in range(n // 2 + 1))
    assert s == lucas(n), n
# funkcje tworzące: (x+2x^2)/(1-x-x^2) = sum_{n>=1} L_n x^n
den = [F(1), F(-1), F(-1)]
num = [F(0), F(1), F(2)]
# szereg num/den: c_n = num_n + c_{n-1} + c_{n-2}
c = []
for n in range(N):
    c.append((num[n] if n < 3 else 0) + (c[n - 1] if n >= 1 else 0) + (c[n - 2] if n >= 2 else 0))
assert c == [F(0)] + [F(lucas(n)) for n in range(1, N)]
# pomocniczo: sum_k C(n-k,k) = F_{n+1}, 1/(1-x-x^2)
fib = [1, 1]  # fib[n] = F_{n+1}
for _ in range(400):
    fib.append(fib[-1] + fib[-2])


def fib_n(k):
    """k-ta liczba Fibonacciego (F_0 = 0, F_1 = 1)."""
    return 0 if k == 0 else fib[k - 1]


for n in range(40):
    assert sum(math.comb(n - k, k) for k in range(n // 2 + 1)) == fib[n]
print("ok  zad4")


# Zadania 5-8: z definicji liczymy E, Var, F(z), G(t) i porównujemy ze wzorami
def moments(dist):
    e = sum(F(j) * p for j, p in dist.items())
    e2 = sum(F(j) ** 2 * p for j, p in dist.items())
    return e, e2 - e * e


def pgf(dist, z):
    return sum(p * z**j for j, p in dist.items())


def mgf(dist, t):
    return sum(float(p) * math.exp(j * t) for j, p in dist.items())


def deriv(f, x, h=1e-4):
    return (f(x + h) - f(x - h)) / (2 * h), (f(x + h) - 2 * f(x) + f(x - h)) / h**2


# Zadanie 5: Var = G''(0) - G'(0)^2 = (ln G)''(0)  (na przykładzie)
dist5 = {0: F(1, 5), 2: F(1, 2), 7: F(3, 10)}
e, v = moments(dist5)
g1, g2 = deriv(lambda t: mgf(dist5, t), 0.0)
assert abs(g1 - float(e)) < 1e-6 and abs(g2 - float(v + e * e)) < 1e-4
_, lg2 = deriv(lambda t: math.log(mgf(dist5, t)), 0.0, 1e-3)
assert abs(lg2 - float(v)) < 1e-4
print("ok  zad5")

# Zadanie 6: rozkład jednostajny na {1..n}
for n in range(1, 15):
    dist = {j: F(1, n) for j in range(1, n + 1)}
    e, v = moments(dist)
    assert e == F(n + 1, 2) and v == F(n * n - 1, 12), n
    for z in [F(2), F(-1, 3), F(5, 7)]:
        if z != 1:
            assert pgf(dist, z) == z * (z**n - 1) / (n * (z - 1))
    for t in [0.3, -0.7, 1.1]:
        assert abs(mgf(dist, t) - math.exp(t) * (math.exp(n * t) - 1) / (n * (math.exp(t) - 1))) < 1e-9
    # F'(1) i F''(1) ze wzoru zwartego na szereg
    f1 = sum(F(j) * p for j, p in dist.items())
    f2 = sum(F(j * (j - 1)) * p for j, p in dist.items())
    assert f1 == F(n + 1, 2) and f2 == F(n * n - 1, 3)
    assert f2 + f1 - f1 * f1 == F(n * n - 1, 12)
print("ok  zad6")

# Zadanie 7: rozkład dwumianowy
for n in range(1, 12):
    for p in [F(1, 3), F(1, 2), F(9, 10)]:
        dist = {j: math.comb(n, j) * p**j * (1 - p) ** (n - j) for j in range(n + 1)}
        e, v = moments(dist)
        assert e == n * p and v == n * p * (1 - p)
        for z in [F(2), F(-1, 3)]:
            assert pgf(dist, z) == (1 - p + p * z) ** n
        for t in [0.3, -0.7]:
            assert abs(mgf(dist, t) - (1 - float(p) + float(p) * math.exp(t)) ** n) < 1e-9
        g1, g2 = deriv(lambda t: math.log((1 - float(p) + float(p) * math.exp(t)) ** n), 0.0, 1e-3)
        assert abs(g1 - float(e)) < 1e-6 and abs(g2 - float(v)) < 1e-4
print("ok  zad7")

# Zadanie 8: rozkład geometryczny (j = 1, 2, ...), obcięty daleko
for p in [F(1, 2), F(1, 3), F(3, 4)]:
    q = 1 - p
    J = 400
    dist = {j: q ** (j - 1) * p for j in range(1, J)}
    e, v = moments(dist)
    assert abs(float(e) - 1 / float(p)) < 1e-9
    assert abs(float(v) - float(q) / float(p) ** 2) < 1e-9
    for z in [F(1, 2), F(-1, 2)]:
        assert abs(float(pgf(dist, z)) - float(p * z / (1 - q * z))) < 1e-9
    t = 0.2 * math.log(1 / float(q))  # t < ln(1/q)
    assert abs(mgf(dist, t) - float(p) * math.exp(t) / (1 - float(q) * math.exp(t))) < 1e-9
    f1 = lambda z: p / (1 - q * z) ** 2
    f2 = lambda z: 2 * p * q / (1 - q * z) ** 3
    assert f1(1) == 1 / p and f2(1) == 2 * q / p**2
    assert f2(1) + f1(1) - f1(1) ** 2 == q / p**2
# obcięty rozkład "j = 1..n" nie jest rozkładem: suma = 1 - (1-p)^n < 1
p, n = F(1, 3), 6
assert sum((1 - p) ** (j - 1) * p for j in range(1, n + 1)) == 1 - (1 - p) ** n < 1
print("ok  zad8")

# Zadanie 9: G(x,y) = 1/(1 - xy - x^2); G_{n,m} = C((n+m)/2, m) gdy n-m parzyste, m <= n
SQ5 = math.sqrt(5)
phi = (1 + SQ5) / 2
Gnm = {}
for n in range(0, 16):
    cnt = {}
    for k in range(0, n + 1):  # długość ciągu
        for seq in itertools.product((1, 2), repeat=k):
            if sum(seq) == n:
                m = seq.count(1)
                cnt[m] = cnt.get(m, 0) + 1
    Gnm[n] = cnt
    for m in range(n + 1):
        twos, rem = divmod(n - m, 2)
        expected = math.comb(m + twos, m) if rem == 0 else 0
        assert cnt.get(m, 0) == expected, (n, m)
    assert sum(cnt.values()) == fib[n]  # G_n = F_{n+1}
    # oczekiwana liczba jedynek: dokładny wzór i asymptotyka
    tot = sum(m * c for m, c in cnt.items())
    E = F(tot, sum(cnt.values()))
    assert E == F((n + 1) * lucas(n + 1) - fib[n], 5 * fib[n])
    assert abs(float(E) - n / SQ5) <= 1 / SQ5 - 1 / 5 + 1e-9 + n * phi ** (-2 * n) * 3, n
# rekurencja h_n = h_{n-1} + h_{n-2} + F_n (F_n = G_{n-1}) i wzór zwarty dla dużych n
h = [0, 1]
for n in range(2, 300):
    h.append(h[-1] + h[-2] + fib_n(n))
for n in range(1, 300):
    assert 5 * h[n] == (n + 1) * lucas(n + 1) - fib_n(n + 1), n
for n in [30, 50, 100, 250]:
    En = F(h[n], fib_n(n + 1))
    assert abs(float(En) - ((n + 1) / SQ5 - 1 / 5)) < 1e-9, n
    assert abs(float(En) - n / SQ5) < 1, n
# rozkład D = x/Q^2 = (2-x)/5 Phi' - 2/5 Phi, Phi = 1/Q = sum F_{n+1} x^n
Phi = [F(fib[n]) for n in range(N + 1)]
dPhi = [(n + 1) * Phi[n + 1] for n in range(N)]  # = (n+1) F_{n+2}
assert all(dPhi[n] == (n + 1) * fib[n + 1] for n in range(N))
D = [F(2, 5) * dPhi[n] - F(1, 5) * (dPhi[n - 1] if n else 0) - F(2, 5) * Phi[n] for n in range(N)]
assert D == [F(h[n]) for n in range(N)]
# (1+2x)^2 + 4(1-x-x^2) = 5
assert [a + 4 * b for a, b in zip([1, 4, 4], [1, -1, -1])] == [5, 0, 0]
for n in range(300):
    assert 5 * h[n] == 2 * (n + 1) * fib[n + 1] - (n + 2) * fib[n], n
# F_{k+1} - phi F_k = psi^k
psi = (1 - SQ5) / 2
for k in range(1, 40):
    assert abs(fib_n(k + 1) - phi * fib_n(k) - psi**k) < 1e-6
print("ok  zad9")

# Przykład z wykładu 3: szukanie maksimum, X_n = liczba wykonań maxi := i
for n in range(1, 8):
    dist = {}
    for perm in itertools.permutations(range(1, n + 1)):
        maxi, x = 0, 0
        for i in range(1, n):
            if perm[i] > perm[maxi]:
                maxi, x = i, x + 1
        dist[x] = dist.get(x, 0) + 1
    tot = math.factorial(n)
    p = {k: F(c, tot) for k, c in dist.items()}
    # rekurencja p_nk = 1/n p_{n-1,k-1} + (n-1)/n p_{n-1,k} przez G_n = prod (z+k-1)/k
    G = [F(1)]
    for k in range(2, n + 1):
        G = [F(k - 1, k) * (G[i] if i < len(G) else 0) + F(1, k) * (G[i - 1] if i >= 1 else 0)
             for i in range(len(G) + 1)]
    assert all(G[k] == p.get(k, 0) for k in range(len(G))), n
    E = sum(k * v for k, v in p.items())
    V = sum(k * k * v for k, v in p.items()) - E * E
    assert E == H(n) - 1, n
    assert V == H(n) - sum((F(1, k * k) for k in range(1, n + 1)), F(0)), n
print("ok  wykład: maksimum (E = H_n - 1, Var = H_n - H_n^(2))")
