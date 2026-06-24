n = int(input("ENTER YOUR NUMBER "))
d = 1
sum=0
while(d<=n):
    sum +=d
    d+=1

print(sum)


n = int(input("ENTER YOUR NUMBER "))
k = 1
for i in range(1,n+1):
    k *= i

print(f"the factorial of {n} is {k}")
print("f.factorial of n{k}")
