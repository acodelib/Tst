__author__ = 'Andrei'


class PhoneBook(object):
    def __init__(self,InitialList = []):
        self.Contacts = InitialList
    def addContact(self,NewContact):
        self.Contacts.append(NewContact)


class Contact(object):
    def __init__(self,Name,Surname,PhoneNo='0'):
        self.Name    = Name
        self.Surname = Surname
        self.PhoneNo = PhoneNo
        self.Details = {}
    def __str__(self):
        return "{} , {} : {}".format(self.Name,self.Surname,self.PhoneNo)


'''
PhList = PhoneBook()
George = Contact("George","Marin", '0860693105')
Mihai = Contact("Mihai","Viteazul","088092256")
PhList.addContact(George)
PhList.addContact(Mihai)
print(George)
print(Mihai)
dir(George)
'''