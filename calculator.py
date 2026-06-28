"""
A small information-processing module used as the "system under test" for the
demo pipeline. A few functions have deliberately seeded defects (analogous to
the paper's mutation-injection methodology, Sec. 4.1) so the pipeline has
real bugs to find, and one function has a signature that will be changed by
`run_demo.py` mid-run to simulate the kind of non-functional break that the
self-healing module is meant to repair.
"""


def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def divide(a, b):
    """Return a divided by b. Raises ZeroDivisionError on b == 0."""
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b


def factorial(n):
    """Return n! for n >= 0. Raises ValueError for negative n."""
    if n < 0:
        raise ValueError("factorial undefined for negative numbers")
    # --- SEEDED DEFECT: off-by-one in the base case (mutation) ---
    if n == 0:
        return 0  # BUG: should be 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def is_prime(n):
    """Return True if n is a prime number, False otherwise."""
    if n < 2:
        return False
    # --- SEEDED DEFECT: range should be n // 2 + 1, off-by-one boundary ---
    for i in range(2, n // 2):  # BUG: misses some divisors at the boundary
        if n % i == 0:
            return False
    return True


def average(numbers):
    """Return the arithmetic mean of a non-empty list of numbers."""
    if not numbers:
        raise ValueError("average() requires a non-empty list")
    return sum(numbers) / len(numbers)
