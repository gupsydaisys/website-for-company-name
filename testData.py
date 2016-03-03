import csv
import random

def getSample():
    n = 20
    with open("dataset1.csv") as f:
        for line in f:
            arr = line.split(", ")
        next = []
        for i, e in enumerate(arr):
            start = e.find("\r")
            if start == -1:
                next.append(e)
            else:
                first = e[0:start]
                last = e[start+1:]
                if ("\r" not in first) and ("\r" not in last):
                    next.append(first)
                    next.append(last)
                else:
                    next.append("medimmune.com")
                    next.append("University of North Carolina at Chapel Hill")
        compToWeb = {}
        webToComp = {}
        isCompany = True
        for i in range(len(next)):
            if isCompany:
                compToWeb[next[i]] = next[i+1]
                webToComp[next[i+1]] = next[i]
            isCompany = not isCompany
        return compToWeb, webToComp

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

