
#typecast the input to float
price = float(input("Enter the price of a meal:"))

tip = price * 0.16
total = price + tip

#format the output to be displayed as money with 2 decimal 
print("A 16% tip would be", "${:,.2f}".format(tip))
print("The total including tip would be", "${:,.2f}".format(total))
