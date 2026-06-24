# def greet():
#     print("how are u ")

# greet()

# def bio(name,age):
#     print(f"HI MY NAME IS {name} AND AGE IS {age}")

# bio(age=12,name="WALI")

def pall(name):
    rev = ""
    for i in range(len(name)-1,-1,-1):
        rev = rev+name[i]
    
    
    if rev == name:
        print("pall")
    else:
        print("NOT A PALL")

pall("NAMAN")
pall("ACTUALLY")



