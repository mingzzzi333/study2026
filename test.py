for i in range(6):
    print("*")
    for j in range(6, -1, -1):
        if i >= j:
            print(" ", end="")

for i in range(6):
    for j in range(i + 1):
        print("*", end="")
    print()