"""
Proof of optimization correctness and performance gains.

This file can be safely deleted. It exists only to demonstrate that the
optimizations produce identical results to the original implementations
and to show the performance improvements.

Run with: python -m shortuuid.verify_optimizations
"""

import sys
import timeit
from typing import List
from uuid import uuid4

from shortuuid.main import int_to_string
from shortuuid.main import ShortUUID
from shortuuid.main import string_to_int as string_to_int_optimized


# =============================================================================
# Original (unoptimized) implementations for comparison
# =============================================================================


def string_to_int_original(string: str, alphabet: List[str]) -> int:
    """Original O(m*n) implementation using list.index()."""
    number = 0
    alpha_len = len(alphabet)
    for char in string:
        number = number * alpha_len + alphabet.index(char)
    return number


def get_alphabet_original(alphabet: List[str]) -> str:
    """Original O(n) implementation that joins on every call."""
    return "".join(alphabet)


# =============================================================================
# Correctness verification
# =============================================================================

ALPHABETS = [
    list("01"),  # Binary
    list("0123456789"),  # Decimal
    list("0123456789abcdef"),  # Hex
    list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"),  # Default
    list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"),  # Base64
]


def verify_string_to_int():
    """Verify string_to_int produces identical output for all inputs."""
    for alphabet in ALPHABETS:
        test_strings = [
            alphabet[0],
            "".join(alphabet[:5]),
            "".join(alphabet[-5:]),
            "".join(alphabet),
        ]

        for _ in range(10):
            u = uuid4()
            encoded = int_to_string(u.int, alphabet, padding=22)
            test_strings.append(encoded)

        alphabet_index = {char: idx for idx, char in enumerate(alphabet)}

        for string in test_strings:
            original = string_to_int_original(string, alphabet)
            optimized_no_cache = string_to_int_optimized(string, alphabet, None)
            optimized_cached = string_to_int_optimized(string, alphabet, alphabet_index)

            assert original == optimized_no_cache
            assert original == optimized_cached


def verify_get_alphabet():
    """Verify get_alphabet returns identical string."""
    for alphabet in ALPHABETS:
        su = ShortUUID("".join(alphabet), dont_sort_alphabet=True)
        original = get_alphabet_original(alphabet)
        optimized = su.get_alphabet()
        assert original == optimized


def verify_roundtrip():
    """Verify full encode/decode roundtrip works correctly."""
    for alphabet in ALPHABETS:
        su = ShortUUID("".join(alphabet))
        for _ in range(100):
            original_uuid = uuid4()
            encoded = su.encode(original_uuid)
            decoded = su.decode(encoded)
            assert original_uuid == decoded


# =============================================================================
# Performance benchmarks
# =============================================================================


def benchmark_string_to_int():
    """Benchmark string_to_int: O(m*n) vs O(m)."""
    alphabet = list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
    test_string = "CXc85b4rqinB7s5J52TRYb"

    original_time = timeit.timeit(
        lambda: string_to_int_original(test_string, alphabet),
        number=10000,
    )

    optimized_no_cache_time = timeit.timeit(
        lambda: string_to_int_optimized(test_string, alphabet, None),
        number=10000,
    )

    alphabet_index = {char: idx for idx, char in enumerate(alphabet)}
    optimized_cached_time = timeit.timeit(
        lambda: string_to_int_optimized(test_string, alphabet, alphabet_index),
        number=10000,
    )

    return original_time, optimized_no_cache_time, optimized_cached_time


def benchmark_get_alphabet():
    """Benchmark get_alphabet: O(n) vs O(1)."""
    alphabet = list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
    su = ShortUUID()

    original_time = timeit.timeit(
        lambda: get_alphabet_original(alphabet),
        number=100000,
    )

    optimized_time = timeit.timeit(
        lambda: su.get_alphabet(),
        number=100000,
    )

    return original_time, optimized_time


def measure_memory_overhead():
    """Measure memory overhead from cached attributes."""
    alphabet = list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")

    alphabet_str = "".join(alphabet)
    str_size = sys.getsizeof(alphabet_str)

    alphabet_index = {char: idx for idx, char in enumerate(alphabet)}
    index_size = sys.getsizeof(alphabet_index)
    for char, idx in alphabet_index.items():
        index_size += sys.getsizeof(char) + sys.getsizeof(idx)

    return {
        "alphabet_str_bytes": str_size,
        "alphabet_index_bytes": index_size,
        "total_overhead_bytes": str_size + index_size,
    }


# =============================================================================
# Main
# =============================================================================


if __name__ == "__main__":
    print("=" * 70)
    print("CORRECTNESS VERIFICATION")
    print("=" * 70)

    print("\nVerifying string_to_int...", end=" ")
    verify_string_to_int()
    print("OK")

    print("Verifying get_alphabet...", end=" ")
    verify_get_alphabet()
    print("OK")

    print("Verifying encode/decode roundtrip...", end=" ")
    verify_roundtrip()
    print("OK")

    print("\n" + "=" * 70)
    print("PERFORMANCE BENCHMARKS")
    print("=" * 70)

    print("\n1. string_to_int (O(m*n) -> O(m))")
    print("-" * 40)
    orig, opt_no_cache, opt_cached = benchmark_string_to_int()
    print(f"   Original (list.index):     {orig*1000:.2f} ms (10k iterations)")
    print(f"   Optimized (build dict):    {opt_no_cache*1000:.2f} ms (10k iterations)")
    print(f"   Optimized (cached dict):   {opt_cached*1000:.2f} ms (10k iterations)")
    print(f"   Speedup (standalone):      {orig/opt_no_cache:.1f}x faster")
    print(f"   Speedup (class-based):     {orig/opt_cached:.1f}x faster")

    print("\n2. get_alphabet (O(n) -> O(1))")
    print("-" * 40)
    orig, opt = benchmark_get_alphabet()
    print(f"   Original:  {orig*1000:.2f} ms (100k iterations)")
    print(f"   Optimized: {opt*1000:.2f} ms (100k iterations)")
    print(f"   Speedup:   {orig/opt:.1f}x faster")

    print("\n3. Memory Overhead (per ShortUUID instance)")
    print("-" * 40)
    mem = measure_memory_overhead()
    print(f"   _alphabet_str:   {mem['alphabet_str_bytes']:4d} bytes")
    print(f"   _alphabet_index: {mem['alphabet_index_bytes']:4d} bytes")
    print(f"   Total overhead:  {mem['total_overhead_bytes']:4d} bytes")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
These optimizations trade a small amount of memory (~6 KB per instance)
for significant CPU performance improvements:

- string_to_int:  list.index() O(n) -> dict lookup O(1)
- get_alphabet:   "".join() on every call -> return cached string
""")
