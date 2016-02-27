import csv
import random

def getNCompanies(n=20):
    n = 20 if n < 1 or n > 947 else int(n)
    with open("companies.txt") as f:
        s = random.sample(range(1, 947), n)
        i = 1
        arr = []
        for line in f:
            if i in s:
                data = line.strip('\n').replace("\x00", "")[:-1]
                if data[0] == "\"":
                    data = data[1:len(data)-1]
                arr.append(data)
            i += 1
    return arr
