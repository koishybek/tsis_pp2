def is_palindrome(s):
    s = ''.join(s.lower().split())  
    return s == s[::-1]

print(is_palindrome(input()))
