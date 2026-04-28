x=int(input("Enter a number: "))
y=int(input("Enter another number: "))
z=int(input("Enter a third number: "))
if (x>y) and (x>z):
    print("x is greater")
elif (y>x) and (y>z):
    print("y is greater")
else:
    print("z is greater.")