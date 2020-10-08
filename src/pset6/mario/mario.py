from cs50 import get_int

n = 0
while n < 1 or n > 8:
    n = int(get_int("Height: "))

for i in range(n):
    for j in range(n):
        if n - i - j <= 1:
            print("#", end="")
        else:
            print(" ", end="")
    print("  ", end="")
    for j in range(i + 1):
        print("#", end = "")
    print()
