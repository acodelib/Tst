__author__ = 'Andrei'
import backend_ops
import json

Pb_Path = 'C:/Users/Andrei/Desktop/PhoneBook.txt'

PB_Obj  = backend_ops.loadPhoneBook(Pb_Path)

Cinput = input('Please choose an initial ')


backend_ops.addPearson(PB_Obj,'NeluCoca','5463105','me_@yahoo.com')

backend_ops.printPhoneBook(PB_Obj)

backend_ops.savePhoneBookSession(PB_Obj,Pb_Path)







