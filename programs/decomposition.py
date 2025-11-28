# Décomposition en produits de facteurs premiers

from math import *


# Do precalculate ?
PRE_CALCULATE = False
# Precalculate limit
LIMIT_SIEVE = 200000


found_primes = [2, 3]
last_prime_sqrt_index = 0


def parse_expr(s):
  try:
    v = int(eval(s))
  except Exception:
    return None
  else:
    return v


def update_sqrt_index(number):
  global last_prime_sqrt_index
  # Update the sqrt index, faster prime detection
  while found_primes[last_prime_sqrt_index] ** 2 <= number:
    last_prime_sqrt_index += 1


def generate_primes_sieve(limit):
  # Sieve of Atkin from GeeksForGeeks.com
  sieve = [False] * (limit + 1)
  x = 1
  while x * x <= limit:
    y = 1

    while y * y <= limit:

      # Main part of
      # Sieve of Atkin
      n = (4 * x * x) + (y * y)
      if (n <= limit and (n % 12 == 1 or
          n % 12 == 5)):
        sieve[n] ^= True

      n = (3 * x * x) + (y * y)
      if n <= limit and n % 12 == 7:
        sieve[n] ^= True

      n = (3 * x * x) - (y * y)
      if (x > y and n <= limit and
          n % 12 == 11):
        sieve[n] ^= True
      y += 1
    x += 1

  r = 5
  while r * r <= limit:
    if sieve[r]:
      for i in range(r * r, limit+1, r * r):
        sieve[i] = False

    r += 1

  assert len(found_primes) == 2
  for a in range(5, len(sieve)):
    if sieve[a]:
      found_primes.append(a)

  update_sqrt_index(found_primes[-1])


def generate_primes(limit: int | None = None) -> Iterator[int]:
  if limit is not None and limit <= 2:
    return

  # Yield already generated primes
  if limit is None:
    yield from found_primes
  else:
    for p in found_primes:
      if p >= limit:
        return
      yield p

  # Faster function to determine if prime in this case
  def faster_is_prime() -> bool:
    for q in found_primes[:last_prime_sqrt_index]:
      if number % q == 0:
        return False
    return True

  # Generate primes
  number = found_primes[-1] + 2

  while limit is None or number < limit:
    update_sqrt_index(number)

    # Check if found prime number
    if not faster_is_prime():
      number += 2
      continue

    # Found prime number
    found_primes.append(number)
    yield number
    number += 2


def decompose(number: int) -> dict[int, int]:
  # Edge cases
  if number == 0:
    return {0: 1}
  if number == 1:
    return {1: 1}

  # Found a divisor
  def found_divisor(divisor):
    nonlocal number
    factors.setdefault(divisor, 0)
    factors[divisor] += 1
    number //= divisor

  # Decompose the number
  factors = {} if number >= 0 else {-1: 1}
  number = abs(number)

  for p in generate_primes():
    # Check if found divisors
    while number % p == 0:
      found_divisor(p)

    # Check until the sqrt of the number
    if p ** 2 > number:
      if number != 1:
        found_divisor(number)
      break

    # If reduced to 1, break
    if number == 1:
      break

  return factors


def format_decomposition(decomposed: dict[int, int]) -> str:
  keys = sorted(decomposed.keys())
  factors = []

  if -1 in keys:
    factors.append("-1")
    keys.remove(-1)

  for k in keys:
    factors.append("%d^%d" % (k, decomposed[k]))
  return " * ".join(factors)


def main():
  if PRE_CALCULATE:
    print("Génération des nombres premiers.")
    print("Patientez 5 secondes environ.")
    generate_primes_sieve(LIMIT_SIEVE)
    print(" ")

  print("Decomposition en produit de facteurs premiers.")
  print("Entrez un entier ou 'enter' pour quitter.")

  inp = None
  while inp != "":
    inp = input("    Entier: ")
    if not inp:
      print("Fin du programme.")
      break

    number = parse_expr(inp)
    if number is None:
      print("  L'entrée \"%s\" n'est pas un nombre entier." % inp)
      continue

    if number > LIMIT_SIEVE ** 2:
      print("  Le nombre que vous avez choisi est important.")
      rep = input("  Voulez vous bien décomposer ? ('-' pour oui) ")
      if rep != "-":
        continue

    try:
      decomposed = decompose(number)
    except MemoryError:
      print("  Le nombre d'entrée est trop important (MemoryError).")
      continue

    result = format_decomposition(decomposed)
    print("%d = %s" % (number, result))


main()
