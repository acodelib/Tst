__author__ = 'Andrei'
import json

###########################################################################
def loadPhoneBook(PhoneBook_Path):
    try:
       with open(PhoneBook_Path,'r') as PB_File:
            PB = json.load(PB_File)
            return PB
    except:
        print('Sorry but Phone book path is not available')
        return 0
###########################################################################
def savePhoneBookSession(PhoneBook_Obj,PhoneBook_Paht):
    try:
        with open(PhoneBook_Paht,'w') as PB_File:
            json.dump(PhoneBook_Obj,PB_File)
    except:
        print("We are sorry but phone book could not be loaded")
        return 0
###########################################################################
def loadCallHistory(History_Path):
    '''
    incarca un fisier si intoarce un dictionar de forma Nume:DataApel
    '''
    print('call history loaded')
###########################################################################
def printPhoneBook(PhoneBook_Obj):
    PB = PhoneBook_Obj
    #try:
    print('{:10}, {:10}, {:30}'.format('Name','Phone No','E-Mail @@'))
    print('-----------------------------------------------------------------')
    for nm,details in PB.items():
         print('{:10}, {:10}, {:30}'.format(nm,details[0],details[1]))
    #except:
     #   print('sorry the phone book cant\'t be printed at the moment')
      #  return None
###########################################################################
def addPearson(PhoneBook_Obj,Name,No,Email):
    if len(Name)>10 or len(No)>10 or len(Email)>20:
        print('We are sorry but names and phone no can\'t be larger than 10 Characters')
        return None
    PB = PhoneBook_Obj
    PB[Name]=[No,Email]
    print('addPearson')
###########################################################################
def deletePearson(PhoneBook_Obj,Name):
    print('delete')
###########################################################################

