"""
Benchmarks to measure performance improvements from optimizations.

This script compares the optimized implementations against the original
implementations to demonstrate the performance gains.

Run with: python -m shortuuid.benchmark_optimizations
"""

import sys
import timeit
from typing import List

from shortuuid.main import ShortUUID
from shortuuid.main import string_to_int as string_to_int_optimized


# Original (unoptimized) implementations for comparison


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


# Benchmarks


def benchmark_string_to_int():
    """Benchmark string_to_int: O(m*n) vs O(m)."""
    alphabet = list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
    test_string = "CXc85b4rqinB7s5J52TRYb"  # 22 chars

    # Without pre-computed index (standalone function use)
    original_time = timeit.timeit(
        lambda: string_to_int_original(test_string, alphabet),
        number=10000,
    )

    optimized_no_cache_time = timeit.timeit(
        lambda: string_to_int_optimized(test_string, alphabet, None),
        number=10000,
    )

    # With pre-computed index (class-based use)
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
    # Measure size of cached attributes
    alphabet = list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")

    # _alphabet_str: cached string representation
    alphabet_str = "".join(alphabet)
    str_size = sys.getsizeof(alphabet_str)

    # _alphabet_index: character to index mapping
    alphabet_index = {char: idx for idx, char in enumerate(alphabet)}
    index_size = sys.getsizeof(alphabet_index)
    # Add size of keys and values
    for char, idx in alphabet_index.items():
        index_size += sys.getsizeof(char) + sys.getsizeof(idx)

    return {
        "alphabet_str_bytes": str_size,
        "alphabet_index_bytes": index_size,
        "total_overhead_bytes": str_size + index_size,
    }


def run_benchmarks():
    """Run all benchmarks and print results."""
    print("=" * 70)
    print("OPTIMIZATION BENCHMARKS")
    print("=" * 70)

    # string_to_int
    print("\n1. string_to_int (O(m*n) -> O(m))")
    print("-" * 40)
    orig, opt_no_cache, opt_cached = benchmark_string_to_int()
    print(f"   Original (list.index):     {orig*1000:.2f} ms (10k iterations)")
    print(f"   Optimized (build dict):    {opt_no_cache*1000:.2f} ms (10k iterations)")
    print(f"   Optimized (cached dict):   {opt_cached*1000:.2f} ms (10k iterations)")
    print(f"   Speedup (standalone):      {orig/opt_no_cache:.1f}x faster")
    print(f"   Speedup (class-based):     {orig/opt_cached:.1f}x faster")

    # get_alphabet
    print("\n2. get_alphabet (O(n) -> O(1))")
    print("-" * 40)
    orig, opt = benchmark_get_alphabet()
    speedup = orig / opt
    print(f"   Original:  {orig*1000:.2f} ms (100k iterations)")
    print(f"   Optimized: {opt*1000:.2f} ms (100k iterations)")
    print(f"   Speedup:   {speedup:.1f}x faster")

    # Memory overhead
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

These optimizations are most beneficial when:
- Encoding/decoding many UUIDs (typical use case)
- Using custom alphabets with many characters
- Calling get_alphabet() frequently (e.g., logging, debugging)
""")


if __name__ == "__main__":
    run_benchmarks()
