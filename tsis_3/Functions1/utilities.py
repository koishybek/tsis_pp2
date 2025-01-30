import math
import random

def grams_to_ounces(grams):
    return grams / 28.3495231

def fahrenheit_to_celsius(f):
    return (5 / 9) * (f - 32)

def sphere_volume(radius):
    return (4/3) * math.pi * (radius ** 3)

def is_palindrome(s):
    s = ''.join(s.lower().split())  
    return s == s[::-1]

def histogram(lst):
    for num in lst:
        print('*' * num)

def guess_the_number():
    name = input()
    number_to_guess = random.randint(1, 20)
    attempts = 0

    print("Well", name, "thinking of a number between 1 and 20.")
    
    while True:
        guess = int(input("Take a guess"))
        attempts += 1

        if guess < number_to_guess:
            print("Your guess is too low.")
        elif guess > number_to_guess:
            print("Your guess is too high.")
        else:
            print("Good job", name," You guessed my number in", attempts," guesses!")
            break