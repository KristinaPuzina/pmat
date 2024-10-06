#!/usr/bin/python3
import math

try:
    x = int(input())

    with open("output.txt", "a") as f:
        print(math.sqrt(x), file=f)

except ValueError as e:
    print(e)

    with open("errors.txt", "a") as f:
        print(e, file=f)
