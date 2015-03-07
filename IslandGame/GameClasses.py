__author__ = 'Andrei'
import random

# #########################################################################
class Island(object):
    def __init__(self, H, L, Predators=0, Preys=0):
        self.Grid = []
        self.H = H
        self.L = L
        #generate empty island grid:
        for i in range(0, H):
            row = [0] * L
            self.Grid.append(row)
            #Add predators
        if Predators != 0:
            for i in range(0, Predators):
                self.RandX = random.randint(0, self.H - 1)
                self.RandY = random.randint(0, self.L - 1)
                #print("X = {}, Y = {}".format(self.RandX,self.RandY))
                while self.Grid[self.RandX][self.RandY] != 0:
                    self.RandX = random.randint(0, self.H - 1)
                    self.RandY = random.randint(0, self.L - 1)
                self.createAnimal("Predator", self.RandX, self.RandY)
        #Add prey
        if Preys != 0:
            for i in range(0, Preys):
                self.RandX = random.randint(0, self.H - 1)
                self.RandY = random.randint(0, self.L - 1)
                #print("X = {}, Y = {}".format(self.RandX,self.RandY))
                while self.Grid[self.RandX][self.RandY] != 0:
                    self.RandX = random.randint(0, self.H - 1)
                    self.RandY = random.randint(0, self.L - 1)
                self.createAnimal("Prey", self.RandX, self.RandY)
        self.scanZoo()
        print("Island initialised:")
        print(self)

    #________________________________________________________________________
    def scanZoo(self):
        self.Zoo = []
        for rw in range(0, self.H):                 #iterate rows
            for cl in range(0, self.L):             #iterate cols
                if self.Grid[rw][cl] != 0:
                    self.Zoo.append(self.Grid[rw][cl])

    #________________________________________________________________________
    def __str__(self):
        Printer = ""
        for rw in range(0, self.H):  #iterate rows
            for cl in range(0, self.L):  #iterate cols
                if self.Grid[rw][cl] != 0:
                    Printer = Printer + "{:<2s}".format(str(self.Grid[rw][cl]))
                else:
                    Printer = Printer + "{:<2s}".format(".")
            Printer = Printer + "\n"
        return Printer

    #________________________________________________________________________
    def createAnimal(self, CreatureType, X, Y):
        if CreatureType == "Predator":
            Ret = Predator(X, Y,self)
            self.Grid[X][Y] = Ret
        else:
            Ret = Prey( X, Y,self)
            self.Grid[X][Y] = Ret
    #________________________________________________________________________
    def registerAnimal(self,SomeAnimal):
        self.Grid[SomeAnimal.X][SomeAnimal.Y] = SomeAnimal
    #________________________________________________________________________
    def tickTack(self):
        for animal in self.Zoo:
            animal.clockTick()
    #________________________________________________________________________
    def echoLocation(self,X,Y):
        if X < 0 or Y < 0 or X > self.H - 1 or Y > self.L - 1:
            return "Outside"
        elif self.Grid[X][Y] == 0:
            return "Free"
        else:
            SpotedCreature = self.Grid[X][Y]
            return str(type(SpotedCreature).__name__)
    #________________________________________________________________________

    def discardPrey(self, H, L, Killer):
        self.Grid[H][L] = 0
    #________________________________________________________________________
##########################################################################
class Animal(object):
    def __init__(self, X, Y,Teritory : "Island", Species="Animal" ):
        self.Species   = Species
        self.X         = X
        self.Y         = Y
        self.BreedTime = 10
        self.Pin       = Species[0]
        self.Teritory  = Teritory
    #________________________________________________________________________
    def learnTeritory(self, Teritory : "Island"):
        self.Teritory = Teritory

    #________________________________________________________________________
    def scanLocation(self, X, Y):
        return self.Teritory.echoLocation(X,Y)
    #________________________________________________________________________
    def makeDecision(self, Finding,X,Y):                    #decides what to do given choices
        if self.BreedTime <= 0 and Finding == "Free":
            self.breed(X,Y)
        elif Finding == "Free":
            self.move(X,Y)
    #________________________________________________________________________
    def breed(self,X,Y):
        MyType = str(type(self).__name__)
        Cub = globals()[MyType](X,Y,self.Teritory)
        self.Teritory.registerAnimal(Cub)
    #________________________________________________________________________
    def move(self, X, Y):
        OldX = self.X
        OldY = self.Y
        self.X = X
        self.Y = Y
        self.Teritory.Grid[X][Y]        = self           # Animal mooves to new position
        self.Teritory.Grid[OldX][OldY]  = 0              # Old position becomes 0
    #________________________________________________________________________
    def die(self):
        self.Teritory.Grid [self.X][self.Y] = 0
    #________________________________________________________________________
    def clockTick(self):
        self.instictMoove()
        self.BreedTime -= 1
    #________________________________________________________________________
    def __str__(self):
        return self.Pin

    #________________________________________________________________________
    def status(self):
        print("{} has {} breed time left".format(self.Species, self.BreedTime))
    #________________________________________________________________________
    def instictMoove(self):
        Alt = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  #Alternatives
        Itr = random.randint(0, 7)
        for Itm in range(0, 8):
            Loc = Alt[Itr]
            TX = self.X + Loc[0]
            TY = self.Y + Loc[1]
            Finding = self.scanLocation(TX, TY)
            '''
            try:
                print("last scaned X = {} and Y = {} and had a {}".format(TX,TY,self.Teritory.Grid[TX][TY]))
            except IndexError:
                print("last scaned X = {} and Y = {} and was outside".format(TX,TY))
            '''
            if Finding != "Outside":
                if self.makeDecision(Finding,TX,TY) > 0:
                    return 1
            if Itr == 7:
                Itr = 0
            else:
                Itr += 1
        return -1
##########################################################################
class Predator(Animal):
    def __init__(self,x,y, teritory, species="Wolf"):
        self.FeedTime = 4
        Animal.__init__(self, x, y,teritory,species)
    #________________________________________________________________________
    def eat(self,a_prey_x,a_prey_y):
        a_prey = self.Teritory.Grid[a_prey_x][a_prey_y]
        self.FeedTime = 4
        self.Teritory.Grid[self.X][self.Y] = 0
        self.X        = a_prey.X
        self.Y        = a_prey.Y
        a_prey.die()
        self.Teritory.registerAnimal(self)
    #________________________________________________________________________
    def makeDecision(self, Finding,X,Y):
        if self.FeedTime < 4 and Finding == "Prey":
            self.eat(X,Y)
            return 1
        elif self.BreedTime <= 0 and Finding == "Free":
            self.breed(X,Y)
            return 1
        elif Finding == "Free":
            self.move(X,Y)
            return 1
        return -1
    #________________________________________________________________________
    def clockTick(self):
        if self.FeedTime < 0:
            self.die()
            return 0
        Animal.clockTick(self)
        self.FeedTime -= 1
    #________________________________________________________________________
##########################################################################
class Prey(Animal):
    def __init__(self, x,y,teritory,species = "Moose"):
        Animal.__init__(self, x, y, teritory, species)
    #________________________________________________________________________
    def makeDecision(self, Finding,X,Y):                    #decides what to do given choices
        if self.BreedTime <= 0 and Finding == "Free":
            self.breed(X,Y)
            return 1
        elif Finding == "Free":
            self.move(X,Y)
            return 1
        else:
            return -1
##########################################################################

#internal testing
if __name__ == '__main__':
    Imb = Island(10, 10, 10, 10)
    for i in range(0,10000):
        Imb.tickTack()
    print(i)
    print(Imb)
else:
    print("module {} has been imported".format(__name__))
