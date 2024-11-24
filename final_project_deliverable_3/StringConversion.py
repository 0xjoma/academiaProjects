#Utility methods to convert text string to/from equivalent "binary digit" strings and to/from integers
#Based on snippets from askpython.com and stackoverflow

import math

#utility methods for xor'ing and padding strings
#-------------------------------------------------------------
#add 0s in front of the binary string X to yield a B-bit string
def pad(X,B):
    return X.rjust(B * math.ceil(len(X)/B),'0')

#xor implemented between two binary strings    
def xor(a,b):
	#a, b binary strings of identical length
    c =[]
    for i in range(0,len(a)):
        if (a[i]=='1' and b[i]=='1') or (a[i]=='0' and b[i]=='0'):
            #print(a[i], b[i], "0" )
            c.append('0')
        else:
            #print(a[i], b[i], "1" )
            c.append('1')
    return ''.join(c)
#-------------------------------------------------------------


#string input, output is integer
def stringToInteger(strg):
    bstrg = stringToBinaryString(strg)
    return binaryStringToInteger(bstrg)

#"binary" string input, output is integer
def binaryStringToInteger(bstrg):
    return int(bstrg, 2)

#string input, output is "binary" string    
def stringToBinaryString(strg):
    bstrg = ''.join(format(ord(c), '08b') for c in strg)
    return bstrg

#"binary" string input, output is string     
def binaryStringToString(bstrg):
    newstrg=''.join(chr(int(bstrg[i*8:i*8+8],2)) for i in range(len(bstrg)//8))
    return newstrg

#integer input, output is "binary" string, adjusted to make desired length, default is multiple of 8
def integerToBinaryString(num, desired_len=None):
    bstrg = bin(num)[2:]
    #prepend to make desired length, if necessary
    if desired_len == None:
        #prepend to make multiple of 8 if necessary
        desired_len = 8 * math.ceil(len(bstrg)/8) 
    formatStr = '0'+str(desired_len)+'b'
    bstrg = format(num,formatStr)   
    return bstrg

    
#integer input, output is string
def integerToString(num):
    bstrg = integerToBinaryString(num)
    return binaryStringToString(bstrg)
    
def testCases():
    #Test cases
    strg="it's a wonderful life"
    bstrg = stringToBinaryString(strg) 
    print(bstrg)

    newstrg=binaryStringToString(bstrg)
    print(newstrg)

    #note bstrg is type string
    print(type(bstrg))

    #from binary string to integer; will strip out leading zeros that need to be added back later
    num = binaryStringToInteger(bstrg)
    print(num)
    print(type(num))

    #from integer to binary string
    bstrg2 = integerToBinaryString(num)
    print(bstrg2)

    #from binary string to string
    newstrg2=binaryStringToString(bstrg2)
    print(newstrg2)
    
    print(integerToBinaryString(5,15));
    
    print("xortest between arrays", xor(["1", "0","1"],["0", "0","1"]))
   
def main():
    testCases();

    
if __name__ == "__main__":
    main()
