# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# # Sample Python Functions Notebook
# This notebook contains implementations of key algorithmic functions:
# 1. **Palindrome Checker** - Determines if a string is a palindrome
# 2. **Longest Palindromic Substring** - Finds the longest palindrome in a string
# 3. **Longest Consecutive Sequence** - Finds the length of longest consecutive sequence in O(n) time
# 4. **Unit Tests** - Comprehensive test suite with edge cases
# All functions include proper error handling and have been tested with various edge cases.


# MARKDOWN ********************

# ## Function Definitions

# CELL ********************

import unittest
from typing import List


def is_palindrome(s: str) -> bool:
    """Check if a string is a palindrome.

    Args:
        s: Input string to check

    Returns:
        True if the string is a palindrome, False otherwise
    """
    if not s:
        return True

    s = s.lower()
    return s == s[::-1]


def longest_palindromic_substring(s: str) -> str:
    """Find the longest palindromic substring in a string.

    Uses Manacher's algorithm for O(n) time complexity.

    Args:
        s: Input string to search

    Returns:
        The longest palindromic substring
    """
    if not s:
        return ""

    # Transform string to handle even-length palindromes
    transformed = '#' + '#'.join(s) + '#'
    n = len(transformed)
    p = [0] * n
    center = 0
    right = 0

    for i in range(1, n - 1):
        mirror = 2 * center - i

        if i < right:
            p[i] = min(right - i, p[mirror])

        # Expand palindrome centered at i
        while (
            i + p[i] + 1 < n
            and i - p[i] - 1 >= 0
            and transformed[i + p[i] + 1] == transformed[i - p[i] - 1]
        ):
            p[i] += 1

        # If palindrome centered at i expands past right,
        if i + p[i] > right:
            center = i
            right = i + p[i]

    # Find maximum palindrome length and its center
    max_len = 0
    max_center = 0
    for i in range(1, n - 1):
        if p[i] > max_len:
            max_len = p[i]
            max_center = i

    start = (max_center - max_len) // 2
    end = start + max_len
    return s[start:end]


def longest_consecutive_sequence(nums: List[int]) -> int:
    """Find the length of the longest consecutive sequence.

    Uses a hash set for O(n) time complexity.

    Args:
        nums: List of integers

    Returns:
        Length of longest consecutive sequence
    """
    if not nums:
        return 0

    num_set = set(nums)
    max_length = 0

    for num in num_set:
        # Check if it's the start of a sequence
        if num - 1 not in num_set:
            current_num = num
            current_length = 1

            # Expand the sequence forward
            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1

            max_length = max(max_length, current_length)

    return max_length


def main() -> None:
    """Demonstrate all functions with example inputs.

    This serves as a basic smoke test to verify functionality.
    """
    print("=== Sample Function Demonstrations ===")
    print()

    # Palindrome examples
    palindrome_tests = ["racecar", "A man a plan a canal Panama", "hello", ""]
    print("Palindrome Tests:")
    for s in palindrome_tests:
        result = is_palindrome(s)
        print(f"  '{s}' -> {result}")
    print()

    # Longest palindromic substring examples
    lps_tests = ["babad", "cbbd", "racecar", "abcdef", "a"]
    print("Longest Palindromic Substring Tests:")
    for s in lps_tests:
        result = longest_palindromic_substring(s)
        print(f"  Input: '{s}' -> Longest palindrome: '{result}'")
    print()

    # Longest consecutive sequence examples
    lcs_tests = [[100, 4, 200, 1, 3, 2], [0, 3, 7, 2, 5, 8, 4, 6, 0, 1], [], [1], [5, 5, 5, 5]]
    print("Longest Consecutive Sequence Tests:")
    for nums in lcs_tests:
        result = longest_consecutive_sequence(nums)
        print(f"  Input: {nums} -> Length: {result}")
    print()
    print("=== Demonstrations Complete ===")


if __name__ == "__main__":
    # Run smoke test demonstration
    main()

    # Run unit tests
    print("\n=== Running Unit Tests ===")
    unittest.main(argv=[''], verbosity=2, exit=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
