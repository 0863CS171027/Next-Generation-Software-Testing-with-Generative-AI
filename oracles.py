"""
Test data ("oracles") used by the offline LLM-template test generator.

In a real deployment these expected values would come from the requirement
specification itself (what the LLM is told the correct behavior should be),
not from peeking at the implementation. Several of the "boundary" expectations
below are intentionally the *correct* mathematical answer even though the
seeded defects in calculator.py will fail to produce it -- that mismatch is
exactly what the defect-detection stage of the pipeline is supposed to catch.
"""

NORMAL_ARGS = {
    "add": (2, 3),
    "divide": (10, 2),
    "factorial": (5,),
    "is_prime": (7,),
    "average": ([2, 4, 6],),
}

BOUNDARY_ARGS = {
    "add": (0, 0),
    "divide": (1, 1),
    "factorial": (0,),
    "is_prime": (4,),
    "average": ([42],),
}

EXCEPTIONAL_ARGS = {
    "add": ("a", 3),          # mismatched types -> TypeError
    "divide": (5, 0),
    "factorial": (-3,),
    "is_prime": ("x",),       # non-numeric input -> TypeError
    "average": ([],),
}

EXPECTED = {
    "add": {"normal": 5, "boundary": 0, "exception": TypeError},
    "divide": {"normal": 5.0, "boundary": 1.0, "exception": ZeroDivisionError},
    "factorial": {"normal": 120, "boundary": 1, "exception": ValueError},  # boundary exposes seeded bug
    "is_prime": {"normal": True, "boundary": False, "exception": TypeError},  # boundary exposes seeded bug
    "average": {"normal": 4.0, "boundary": 42.0, "exception": ValueError},
}
