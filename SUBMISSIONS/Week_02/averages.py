a = float(input("Please enter the first number: "))
b = float(input("Please enter the second number: "))
op = input("Please indicate which type of average you would like to calculate: select from the following options\nType 1 for arithmetic mean\nType 2 for geometric mean\nType 3 for root-mean-square\n")

import math
if op == '1':
    avg = (a+b)/2
    print("Based on the average type you select, the result is", avg) #assignment does not specify the print format, thus the code assumes to output the raw format.
elif op == '2':
    avg = math.sqrt(a*b)
    print("Based on the average type you select, the result is", avg)
elif op == '3':
    avg = math.sqrt((a**2+b**2)/2)
    print("Based on the average type you select, the result is", avg)
         
#error handling process to avoid exceptions even though clear instruction has been provided.
else:
    print("Invalid input. Please try again.")