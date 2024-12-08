#!/usr/bin/python3
import math
import sys

from write_logs import write

try:
    x = float(input())
    write(message=f"x={x}", filename="sqrt.py")

    with open("output.txt", "a") as f:
        print(math.sqrt(x), file=f)

except (ValueError, EOFError) as e:
    print(e, file=sys.stderr)
    exit(1)
