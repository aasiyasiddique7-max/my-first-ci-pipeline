def calc_sum(a,b):
    sum = a/b
    print(sum)
    return sum

calc_sum(3,4)
a = 3
b=4 
sum = a+b
print(sum)

calc_sum(4,3)


a = 4
b=3
sum = a+b
print(sum)


calc_sum(1,2)


a =1
b=2
sum = a+b
print(sum)


def avg(a,b,c):
    o=(a+b+c)/3
    print(o)

avg(5,6,7)
avg(7,3,5)
avg(0,2,4)

nums = [1,3,4,5,6,8,2]
nums2=[1,4,6,2,5,1,5]

def p_nums(list):
    print(len(list))

def usd_val(n):
    inr_val=n*85
    print(n,"THIS IS USD",inr_val,"THIS IS INR CONVERTED")

usd_val(2)

def num(n):
    if n%2==0:
        print("THIS IS EVEN",n)
    else:
        print("THIS IS ODD",n)    

num(2)
num(33)
