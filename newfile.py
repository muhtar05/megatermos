from itertools import product, combinations_with_replacement,combinations,permutations


def comb(n, k):
    """Генерация сочетаний из `n` по `k` без повторений."""

    d = list(range(0, k))
    yield d

    while True:
        i = k - 1
        while i >= 0 and d[i] + k - i + 1 > n:
            i -= 1
        if i < 0:
            return

        d[i] += 1
        for j in range(i + 1, k):
            d[j] = d[j - 1] + 1

        yield d


def comb_sets(sets, m):
    """Генерация сочетаний из элементов множеств `sets` по `m` элементов."""

    for ci in comb(len(sets), m):
        for cj in product(*(sets[i] for i in ci)):
            yield cj


# l1 = ['al', 'bc']
# i = len(l1)
# while i > 0:
#     for c in comb_sets(l1, i):
#         print(c)
#     i -=1

l1 = ['alfa','beta','gamma','delta']
i = len(l1)
while i > 0:
    for el in combinations(l1, i):
        print(el)
    i -=1