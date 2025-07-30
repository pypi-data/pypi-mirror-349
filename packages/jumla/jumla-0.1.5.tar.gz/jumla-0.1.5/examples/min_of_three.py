import inspect
import textwrap


def minOfThree(a: int, b: int, c: int) -> int:
    return min(a, b, c)


function = textwrap.dedent(inspect.getsource(minOfThree))

description_doc = """This task requires writing a Lean 4 method that finds the minimum among three given integers. The method should return the smallest value, ensuring that the result is less than or equal to each of the input numbers and that it is one of the provided integers."""

input_doc = """The input consists of three integers:
a: The first integer.
b: The second integer.
c: The third integer."""

output_doc = """The output is an integer:
Returns the minimum of the three input numbers, assuring that the returned value is less than or equal to a, b, and c, and that it matches one of these values."""

test_cases = [
    {"input": {"a": 3, "b": 2, "c": 1}, "expected": 1, "unexpected": [2, 3, -1]},
    {"input": {"a": 5, "b": 5, "c": 5}, "expected": 5, "unexpected": [-1]},
    {"input": {"a": 10, "b": 20, "c": 15}, "expected": 10, "unexpected": [5]},
    {"input": {"a": -1, "b": 2, "c": 3}, "expected": -1, "unexpected": [2]},
    {"input": {"a": 2, "b": -3, "c": 4}, "expected": -3, "unexpected": [4]},
    {"input": {"a": 2, "b": 3, "c": -5}, "expected": -5, "unexpected": [2]},
    {"input": {"a": 0, "b": 0, "c": 1}, "expected": 0, "unexpected": [1]},
    {"input": {"a": 0, "b": -1, "c": 1}, "expected": -1, "unexpected": [0]},
    {"input": {"a": -5, "b": -2, "c": -3}, "expected": -5, "unexpected": [1, -2]},
]

__all__ = ["function", "description_doc", "input_doc", "output_doc", "test_cases"]
