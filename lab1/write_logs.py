def write(message, filename):
    with open("logs.txt", "a") as f:
        f.write(f"{message} {filename}\n")
