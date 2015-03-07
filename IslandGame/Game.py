__author__ = 'Andrei'

class First(object):
    def __init__(self):
        self.Plm = Second(self)
    def __str__(self):
        return "First"

class Second(object):
    def __init__(self,Ref):
        self.Ref = Ref
    def show(self):
        print(self.Ref)


Flm = globals()['First']()
Flm.Plm.show()
