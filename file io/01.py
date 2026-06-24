# v=open("practice.txt","w")
# v.write('''HI EVERYONE
#         IM LEARNING FILE IO 
#         FROM JAVA ''')
# print(v)

# with open("practice.txt","r") as f:
#     data=f.read()

# v=data.replace("JAVA","PYTHON")
# print(v) 

with open("practice.txt","r") as f:
    data=f.read()
    if(data.find("JAVA") !=-1):
        print("FOUND")
    else:
        print("NOT FOUND")