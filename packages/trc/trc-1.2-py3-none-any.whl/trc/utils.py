# utils.py
# Import packages
import trc

# Helper function for GCD of two numbers
@trc.cache
def gcd_two(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a