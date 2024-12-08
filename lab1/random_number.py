#!/usr/bin/python3
import random

from write_logs import write

a = random.randint(-10, 10)
print(a)
write(message=f"A={a}", filename="random_number.py")
