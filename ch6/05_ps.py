a = int(input("ENTER MARKS"))
b = int(input("ENTER MARKS"))
c = int(input("ENTER MARKS"))

total_percentage = 100*(a+b+c)/300

if(total_percentage>=33):
    print("PASS",total_percentage)

else:
    print("FAIL",total_percentage)

if(a<33):
    print("GIVE RE TEST")

if(b<33):
    print("GIVE RE TEST ")

if(c<33):
    print("REPEAT CLASS")
