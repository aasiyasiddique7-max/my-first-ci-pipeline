r = int(input("ENTER YOUR NUMBER "))
for y in range(2,r):
    if r%y==0:
        print("THIS NUMBER ISNT PRIME")
        break

else:
    print("IT IS PRIME")