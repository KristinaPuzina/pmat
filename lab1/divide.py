#!/usr/bin/python3
import random
import sys

from write_logs import write

try:
    a = int(input())
    b = random.randint(-10, 10)
    print(a / b)
    write(message=f"A={a}, B={b}", filename="divide.py")

except (ZeroDivisionError, ValueError) as e:
    print(e, file=sys.stderr)
    exit(1)
