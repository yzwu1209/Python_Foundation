#get the input from user and make all letters lower case, in case input is mixed with lower and upper case.
name = input("Enter your name: ").lower()
l = len(name) #get the length of the input
k = 1
s = name[l-1].upper()
while k < l:
    s = s+name[l-k-1] #concatenate the string from backward
    k+=1
print(s)
if s.lower() == name.lower(): #compare original input with the reversed string in lower case
    print("Palindrome!")
    
