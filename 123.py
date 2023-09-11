# not optimized

from pprint import pprint


def gen_factors() -> (list, int):
    # https://en.wikipedia.org/wiki/Prime_number

    MIN_FACTOR = 2
    SELF_FACTOR = False
    PRIME_FACTORIZATION_START = 16

    history = {}

    number = 0
    while True:
        total = 0
        factors = []

        number_2 = MIN_FACTOR
        while number_2 < number + (1 if SELF_FACTOR else 0):
            is_factor = number % number_2 == 0
            if is_factor:
                total = total + 1

                if number_2 < number:
                    total = total + history[str(number_2)]

                is_prime = False
                for factor in factors:
                    if number_2 % factor == 0:
                        is_prime = True
                exclude = is_prime and number_2 > PRIME_FACTORIZATION_START
                if not exclude:
                    factors.append(number_2)

            number_2 = number_2 + 1

        # len(factors) != total
        yield (total, factors)

        history[str(number)] = total
        number = number + 1


STOP = 64  # 16 60 64 100 256 1000
EXCLUDE = 1

store = []
for [number, [total, factors]] in enumerate(gen_factors()):
    if total >= EXCLUDE:
        ratio = float(str(total / number)[: 2 + 2])
        store.append([number, ratio, total, factors])

    if number == STOP:
        break

pprint(sorted(store, key=lambda e: e[1]))
