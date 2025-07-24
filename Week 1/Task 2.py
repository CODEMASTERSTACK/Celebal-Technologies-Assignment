value1 = int(input("Enter the 1st Value: "))
value2 = int(input("Enter the 2nd Value: "))

print("Choose options from: '+' , '-', '*', '/' ")
choice = input("Your Choice is: ")

if(choice=='+'):
    print("The addition of your two values is: ", value1+value2)
elif(choice=='-'):
    print("The subtraction of your two values is: ", value1-value2)
elif(choice=='*'):
    print("The multiplication of your two values is: ", value1*value2)
elif(choice=='/'):
    print("The division of your two values is: ", value1/value2)

else:
    print("Wrong input! Check your input and try again.")
