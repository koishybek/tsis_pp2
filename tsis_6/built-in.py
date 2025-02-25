import math
import time
import functools

def multiply_list(numbers):
    return functools.reduce(lambda x, y: x * y, numbers)

def count_case(s):
    upper = sum(1 for c in s if c.isupper())
    lower = sum(1 for c in s if c.islower())
    return upper, lower

def is_palindrome(s):
    return s == s[::-1]

def delayed_sqrt(number, delay_ms):
    time.sleep(delay_ms / 1000)
    return math.sqrt(number)

def all_true(t):
    return all(t)

numbers = [1, 2, 3, 4]
print("Product of list:", multiply_list(numbers))

s = "HelloWorld"
upper, lower = count_case(s)
print(f"Upper case: {upper}, Lower case: {lower}")

s_palindrome = "madam"
print(f"Is palindrome: {is_palindrome(s_palindrome)}")

num, delay = 25100, 2123
print(f"Square root of {num} after {delay} milliseconds is {delayed_sqrt(num, delay)}")

tuple_vals = (True, True, False)
print("All elements are True:", all_true(tuple_vals))
