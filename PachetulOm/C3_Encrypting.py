__author__ = 'Andrei'
'''
this is actualy C4
'''

Keitza        =0
Stringutzul   =""
CharSet       =""
Local         =""
Coded         =""

Keitza = int(input("Please insert coding offset: "))
Stringutzul = input("Please input text to codify: ")

#############################################################################################
#############################################################################################
def Codificator(Key,TheString):
    CharSet     =""
    Local       =""
    Coded       =""
    for elem in TheString:
        CharSet = CharSet + str(ord(elem)+Key)+ "&"

    CharSet = CharSet[0:len(CharSet)]

    for elem in CharSet:
        if elem != '&':
            Local = Local + elem
        else:
            Coded = Coded + chr(int(Local)) #+ " "
            Local = ""
    return Coded
#############################################################################################
#############################################################################################
Astring = Codificator(Keitza,Stringutzul)

print (Astring)

Bstring = Codificator(Keitza*-1,Astring)
print (Bstring)
