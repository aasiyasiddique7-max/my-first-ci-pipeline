a = int(input("ENTER NUMBER 1:"))
b = int(input("ENTER NUMBER 2:"))
c = int(input("ENTER NUMBER 3:"))
d = int(input("ENTER NUMBER 4:"))

if(a>b and a>c and a>d):
    print("a IS THE GREATEST",a)

elif(a<=0):
    print("NUMBER IS INVALID",a)

if(b>a and b>c and b>d):
    print("b IS THE GREATEST",b)

elif(b<=0):
    print("NUMBER IS INVALID",b)

if(c>b and c>a and c>d):
    print("c IS THE GREATEST",c)

elif(c<=0):
    print("NUMBER IS INVALID",c)

if(d>a and d>b and d>c):
    print("d IS THE GREATEST",d)

elif(d<=0):
    print("INVALID NUMBER",d)


# else:
#     print("ALL THE NUMBERS ARE EQUAL")




