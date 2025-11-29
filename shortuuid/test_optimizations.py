"""
Tests to verify optimization correctness and measure performance improvements.

This module compares the optimized implementations against the original
implementations to ensure identical behavior, and benchmarks the performance
gains from the optimizations.

Run with: python -m pytest shortuuid/test_optimizations.py -v
Or standalone: python shortuuid/test_optimizations.py
"""

import sys
import timeit
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4

# Import optimized implementations
from shortuuid.main import int_to_string as int_to_string_optimized
from shortuuid.main import ShortUUID
from shortuuid.main import string_to_int as string_to_int_optimized


# =============================================================================
# Original (unoptimized) implementations for comparison
# =============================================================================


def int_to_string_original(
    number: int, alphabet: List[str], padding: Optional[int] = None
) -> str:
    """Original O(n^2) implementation using string concatenation."""
    output = ""
    alpha_len = len(alphabet)
    while number:
        number, digit = divmod(number, alpha_len)
        output += alphabet[digit]
    if padding:
        remainder = max(padding - len(output), 0)
        output = output + alphabet[0] * remainder
    return output[::-1]


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
# Correctness tests
# =============================================================================


class TestOptimizationCorrectness:
    """Verify optimized implementations produce identical results."""

    # Test with various alphabet sizes
    ALPHABETS = [
        list("01"),  # Binary
        list("0123456789"),  # Decimal
        list("0123456789abcdef"),  # Hex
        list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"),  # Default
        list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"),  # Base64-like
    ]

    def test_int_to_string_identical_results(self):
        """Verify int_to_string produces identical output for all inputs."""
        test_numbers = [
            0,
            1,
            255,
            65535,
            2**32 - 1,
            2**64 - 1,
            2**128 - 1,  # Max UUID value
        ]

        for alphabet in self.ALPHABETS:
            for number in test_numbers:
                for padding in [None, 10, 22, 50]:
                    original = int_to_string_original(number, alphabet, padding)
                    optimized = int_to_string_optimized(number, alphabet, padding)
                    assert original == optimized, (
                        f"Mismatch for number={number}, alphabet_len={len(alphabet)}, "
                        f"padding={padding}: '{original}' != '{optimized}'"
                    )

    def test_string_to_int_identical_results(self):
        """Verify string_to_int produces identical output for all inputs."""
        for alphabet in self.ALPHABETS:
            # Generate test strings using the alphabet
            test_strings = [
                alphabet[0],  # Single char
                "".join(alphabet[:5]),  # First 5 chars
                "".join(alphabet[-5:]),  # Last 5 chars
                "".join(alphabet),  # Full alphabet
            ]

            # Also test with encoded UUIDs
            for _ in range(10):
                u = uuid4()
                encoded = int_to_string_original(u.int, alphabet, padding=22)
                test_strings.append(encoded)

            alphabet_index = {char: idx for idx, char in enumerate(alphabet)}

            for string in test_strings:
                original = string_to_int_original(string, alphabet)
                # Test both with and without pre-computed index
                optimized_no_cache = string_to_int_optimized(string, alphabet, None)
                optimized_cached = string_to_int_optimized(string, alphabet, alphabet_index)

                assert original == optimized_no_cache, (
                    f"Mismatch (no cache) for string='{string}': "
                    f"{original} != {optimized_no_cache}"
                )
                assert original == optimized_cached, (
                    f"Mismatch (cached) for string='{string}': "
                    f"{original} != {optimized_cached}"
                )

    def test_get_alphabet_identical_results(self):
        """Verify get_alphabet returns identical string."""
        for alphabet in self.ALPHABETS:
            su = ShortUUID("".join(alphabet))
            original = get_alphabet_original(alphabet)
            optimized = su.get_alphabet()
            # Note: ShortUUID sorts the alphabet by default
            su_unsorted = ShortUUID("".join(alphabet), dont_sort_alphabet=True)
            optimized_unsorted = su_unsorted.get_alphabet()
            assert original == optimized_unsorted, (
                f"Mismatch: '{original}' != '{optimized_unsorted}'"
            )

    def test_full_encode_decode_roundtrip(self):
        """Verify full encode/decode roundtrip works correctly."""
        for alphabet in self.ALPHABETS:
            su = ShortUUID("".join(alphabet))
            for _ in range(100):
                original_uuid = uuid4()
                encoded = su.encode(original_uuid)
                decoded = su.decode(encoded)
                assert original_uuid == decoded, (
                    f"Roundtrip failed: {original_uuid} -> '{encoded}' -> {decoded}"
                )

    def test_valueerror_preserved(self):
        """Verify ValueError is raised for invalid characters."""
        alphabet = list("abc")
        alphabet_index = {char: idx for idx, char in enumerate(alphabet)}

        try:
            string_to_int_optimized("xyz", alphabet, alphabet_index)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "'x' is not in alphabet" in str(e)


# =============================================================================
# Performance benchmarks
# =============================================================================


def benchmark_int_to_string():
    """Benchmark int_to_string: O(n^2) vs O(n)."""
    alphabet = list("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
    test_number = 2**128 - 1  # Worst case: max UUID value

    original_time = timeit.timeit(
        lambda: int_to_string_original(test_number, alphabet, 22),
        number=10000,
    )

    optimized_time = timeit.timeit(
        lambda: int_to_string_optimized(test_number, alphabet, 22),
        number=10000,
    )

    return original_time, optimized_time


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

    # int_to_string
    print("\n1. int_to_string (O(n²) → O(n))")
    print("-" * 40)
    orig, opt = benchmark_int_to_string()
    speedup = orig / opt
    print(f"   Original:  {orig*1000:.2f} ms (10k iterations)")
    print(f"   Optimized: {opt*1000:.2f} ms (10k iterations)")
    print(f"   Speedup:   {speedup:.1f}x faster")

    # string_to_int
    print("\n2. string_to_int (O(m×n) → O(m))")
    print("-" * 40)
    orig, opt_no_cache, opt_cached = benchmark_string_to_int()
    print(f"   Original (list.index):     {orig*1000:.2f} ms (10k iterations)")
    print(f"   Optimized (build dict):    {opt_no_cache*1000:.2f} ms (10k iterations)")
    print(f"   Optimized (cached dict):   {opt_cached*1000:.2f} ms (10k iterations)")
    print(f"   Speedup (standalone):      {orig/opt_no_cache:.1f}x faster")
    print(f"   Speedup (class-based):     {orig/opt_cached:.1f}x faster")

    # get_alphabet
    print("\n3. get_alphabet (O(n) → O(1))")
    print("-" * 40)
    orig, opt = benchmark_get_alphabet()
    speedup = orig / opt
    print(f"   Original:  {orig*1000:.2f} ms (100k iterations)")
    print(f"   Optimized: {opt*1000:.2f} ms (100k iterations)")
    print(f"   Speedup:   {speedup:.1f}x faster")

    # Memory overhead
    print("\n4. Memory Overhead (per ShortUUID instance)")
    print("-" * 40)
    mem = measure_memory_overhead()
    print(f"   _alphabet_str:   {mem['alphabet_str_bytes']:4d} bytes")
    print(f"   _alphabet_index: {mem['alphabet_index_bytes']:4d} bytes")
    print(f"   Total overhead:  {mem['total_overhead_bytes']:4d} bytes")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
All optimizations trade a small amount of memory (~6 KB per instance)
for significant CPU performance improvements:

- int_to_string:  String concatenation → list.append() + join()
- string_to_int:  list.index() O(n) → dict lookup O(1)
- get_alphabet:   "".join() on every call → return cached string

These optimizations are most beneficial when:
- Encoding/decoding many UUIDs (typical use case)
- Using custom alphabets with many characters
- Calling get_alphabet() frequently (e.g., logging, debugging)
""")


if __name__ == "__main__":
    # Run correctness tests
    print("Running correctness tests...")
    test = TestOptimizationCorrectness()
    test.test_int_to_string_identical_results()
    print("  ✓ int_to_string produces identical results")
    test.test_string_to_int_identical_results()
    print("  ✓ string_to_int produces identical results")
    test.test_get_alphabet_identical_results()
    print("  ✓ get_alphabet produces identical results")
    test.test_full_encode_decode_roundtrip()
    print("  ✓ Full encode/decode roundtrip works")
    test.test_valueerror_preserved()
    print("  ✓ ValueError preserved for invalid input")
    print()

    # Run benchmarks
    run_benchmarks()
