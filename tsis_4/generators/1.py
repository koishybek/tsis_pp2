def square_generator(N):
    for i in range(N + 1):
        yield i ** 2

N = 10
gen = square_generator(N)
for num in gen:
    print(num)
