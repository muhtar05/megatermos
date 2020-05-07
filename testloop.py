import time


def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    print(pool)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    print(indices)
    yield tuple(pool[i] for i in indices)
    while True:
        print("while")
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            print("Return")
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)


def product(*args, repeat=1):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args] * repeat

    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


A = ['a','b','c']
def new_prod(*args):
    pools = [tuple(pool) for pool in args] * 3
    print(pools)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]

    print(result)
    for prod in result:
        yield tuple(prod)


for i in new_prod(A):
    print(i)