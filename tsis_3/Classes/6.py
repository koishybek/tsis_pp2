numbers = [1, 2, 3, 4, 5, 9, 11, 13, 15, 16, 17, 19, 20]

prime_numbers = list(
    filter(
        lambda x: x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1)),
        numbers
    )
)

print(prime_numbers)