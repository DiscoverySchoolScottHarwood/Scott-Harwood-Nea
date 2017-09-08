import random
names = open("first names.txt")
fullnames = []
names = names.readlines()
random.shuffle(names)
count = 0
maxx = len(names)
for x in range(int(len(names)/2)):
    fullnames.append(names[x][:-1] +" "+ names[-x])
    count +=2

namesfile = open("fullnames.txt","w")
for x in fullnames:
    namesfile.write(x)

namesfile.close()
print((count/maxx)*100)
