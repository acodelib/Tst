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
                self.addAnimal("Predator", self.RandX, self.RandY)
        #Add prey
        if Preys != 0:
            for i in range(0, Preys):
                self.RandX = random.randint(0, self.H - 1)
                self.RandY = random.randint(0, self.L - 1)
                #print("X = {}, Y = {}".format(self.RandX,self.RandY))
                while self.Grid[self.RandX][self.RandY] != 0:
                    self.RandX = random.randint(0, self.H - 1)
                    self.RandY = random.randint(0, self.L - 1)
                self.addAnimal("Prey", self.RandX, self.RandY)
        self.scanZoo()
        print("Island initialised:")
        print(self)

    #________________________________________________________________________
    def scanZoo(self):
        self.Zoo = []
        for rw in range(0, self.H):  #iterate rows
            for cl in range(0, self.L):  #iterate cols
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
    def addAnimal(self, CreatureType, X, Y):
        if CreatureType == "Predator":
            Ret = Predator("Wolf", X, Y)
            self.Grid[X][Y] = Ret
        else:
            Ret = Prey("Moose", X, Y)
            self.Grid[X][Y] = Ret

    #________________________________________________________________________
    def tickTack(self):
        for animal in self.Zoo:
            animal.clockTick()
            print(animal.status())
            #________________________________________________________________________

    #________________________________________________________________________
    def check(self, SomeAnimal: "Animal"):
        LH = SomeAnimal.X
        LY = SomeAnimal.Y
        Alt = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  #Alternatives
        Itr = random.randint(0, 7)
        print(Itr)
        for Itm in range(0, 8):
            Loc = Alt[5]  #local variable for storing coordinates tuple
            Finding = self.echoLocation(LH + Loc[0], LY + Loc[1])
            if Finding != "Free" and Finding != "Outside":
                return str(Finding)
            if Itr == 7:
                Itr = 0
            else:
                Itr += Itr
        return "NA"

    #________________________________________________________________________
    def discardPrey(self, H, L, Killer):
        self.Grid[H][L] = 0
        #________________________________________________________________________


##########################################################################
class Animal(object):
    def __init__(self, X, Y, Species="Animal"):
        self.Species = Species
        self.X = X
        self.Y = Y
        self.BreedTime = 10
        self.Pin = Species[0]

    #________________________________________________________________________
    def learnEnvironment(self, IslandGrid):
        self.Home = IslandGrid

    #________________________________________________________________________
    def echoLocation(self, X, Y):
        if X < 0 or Y < 0 or X > self.H - 1 or Y > self.L - 1:
            return "Outside"
        elif self.Grid[X][Y] == 0:
            return "Free"
        else:
            SpotedCreature = self.Grid[X][Y]
            if type(SpotedCreature) == Predator:
                return "Predator"
            else:
                return "Prey"

    #________________________________________________________________________
    def makeDecision(self, Choice):  #decides what to do given choices
        if self.BreedTime <= 0:
            return "Breed"
        elif Choice == "Free":
            return "Move"

    #________________________________________________________________________
    def move(self, X, Y):
        self.X = X
        self.Y = Y

    #________________________________________________________________________
    def clockTick(self):
        self.BreedTime -= 1

    #________________________________________________________________________
    def __str__(self):
        return self.Pin

    #________________________________________________________________________
    def status(self):
        print("{} has {} breed time left".format(self.Species, self.BreedTime))
        #________________________________________________________________________


##########################################################################
class Predator(Animal):
    def __init__(self, Species="Wolf", X, Y):
        self.FeedTime = 4
        Animal.__init__(self, X, Y, Species)

    #________________________________________________________________________
    def eat(self):
        self.FeedTime = 4

    #________________________________________________________________________
    def clockTick(self):
        self.FeedTime -= 1
        Animal.clockTick(self)

    #________________________________________________________________________
    def decide(self, Choice):
        if Choice == "Prey" and self.BreedTime < 4:
            return "Eat"
        elif self.BreedTime <= 0:
            return "Breed"
        else:
            return "Move"
    #________________________________________________________________________


##########################################################################
class Prey(Animal):
    def __init__(self, Species="Moose", X, Y):
        Animal.__init__(self, X, Y, Species)

    ##########################################################################

#internal testing
if __name__ == '__main__':
    Imb = Island(10, 10, 10, 10)
    for i in Imb.Zoo:
        print(Imb.instictMove(i))


else:
    print("module {} has been imported".format(__name__))
