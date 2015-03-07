import string
import httplib2
inNo = int(input("Please type a integer: "))
Binary = ""



while inNo >1:
    i = inNo % 2
    inNo = int(inNo /2)
    Binary = Binary + str(i)


Binary = "1" + Binary[::-1]
#print (Binary)
#I = len(Binary)-1
numToRet = 0
print(Binary)


for i in range(len(Binary),0,-1):
     numToRet +=((2**(i-1)) * int(Binary[-i]))

print (numToRet)





