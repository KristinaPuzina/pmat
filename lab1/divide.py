#!/usr/bin/python3
import random

try:
    a = int(input())
    b = random.randint(-10, 10)
    print(a / b)

except (ZeroDivisionError, ValueError) as e:
    print(e)

    with open("errors.txt", "a") as f:
        print(e, file=f)
