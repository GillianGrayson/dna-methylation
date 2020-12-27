n = int(input())
str = input()
podsub = []
for i in range(len(str) - n + 1):
    podsub.append(str[i: i + n])
podsub = list(podsub)
ind = []
nnn = []
b = len(podsub)
for i in range(b):
    for j in range(b):
        if podsub[i][0: n - 1] == podsub[j][0: n - 1] and i != j: #podsub[i]
            ind.append(i)
            nnn.append(podsub[j])
            podsub[j] = "no"
for i in range(b):
    if podsub[i] != "no":
        print(podsub[i][0:n - 1], end=" -> ")
        print(podsub[i][1: n], end='')
        for j in range(len(ind)):
            if ind[j] == i:
                print(',', nnn[j][1:n], end='')
        print()