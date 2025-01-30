def histogram(lst):
    for num in lst:
        print('*' * num)

histogram(list(map(int, input().split())))
