"""
Tests to verify optimization correctness.

This module compares the optimized implementations against the original
implementations to ensure identical behavior.
"""

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
                encoded = int_to_string(u.int, alphabet, padding=22)
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
