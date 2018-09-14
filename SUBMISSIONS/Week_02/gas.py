
gal = float(input("Please enter a number of gallons of gasoline: "))
ltr = gal * 3.7854
brl = gal / 19.5
price = gal * 3.65

print(gal, "gallons of gasoline are equivalent to", "{:.4f}".format(ltr), "liters.")
print("It requires", "{:.3f}".format(brl), "barrels of oil to produce.") 
print("Its price is", "${:,.2f}".format(price), "in US Dollars.")
