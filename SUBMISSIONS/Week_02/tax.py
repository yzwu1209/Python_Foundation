
income = int(float(input("Please enter your income: "))) #to avoid type error if user input a float. The code assumes user will not input string as stated in the assignment.

if income > 2000:
    tax = 1000*0.05+1000*0.1+(income - 2000)*0.15
    print("The tax owed is:","${:,.0f}".format(tax)) #format the output to be in money format without decimal as shown in the assignment instructions.
elif income >1000 and income <=2000:
    tax = 1000*0.05+(income - 1000)*0.1
    print("The tax owed is:","${:,.0f}".format(tax))
elif income >=0 and income <=1000:
    tax = income * 0.05
    print("The tax owed is:","${:,.0f}".format(tax))
    
#To handle input that is not within the specified range, for example less than zero.
else:
    print("Invalid input. Tax cannot be calculated. Please try again.")
