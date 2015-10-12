import random

class DiceGen(object) :    
    """
    Class for handling rolls in dice games with a given number of N-sided dice.
    """     

    @staticmethod
    def sOneRoll(numDice, numSides, randGen = random.randint) :
        """
        Returns a list of rolled dice values
        
        numDice: number of dice in the roll
        numSides: number of sides per die
        randGen: a function that returns a random integer with same signature as
                 random.randint
        """
        rtv = []
        for i in range(numDice) :
            rtv.append(randGen(1, numSides))
        return rtv

    @staticmethod
    def sAllRolls(numDice, numSides) :
        """
        Generates all possible combinations of dice rolls 
        
        numDice: number of dice in the roll
        numSides: number of sides per die
        """
        dice = [1] * numDice
        stopIter = numDice * numSides
        while True:
            yield dice
            if ( sum(dice) == stopIter ) :
                raise StopIteration
            for i in range(numDice) :
                if dice[i] < numSides :
                    dice[i] = dice[i] + 1
                    break;
                else :
                    dice[i] = 1
                    
    def __init__(self, numDice, numSides, randGen = random.randint) :
        """
        Constructor 
        
        numDice: number of dice in the roll
        numSides: number of sides per die
        randGen: a function that returns a random integer with same signature as
                 random.randint
        """
        self.NumDice = numDice
        self.NumSides = numSides
        self.RandGen = randGen

    def OneRoll(self, holding=0) :
        """
        Returns a list of rolled dice values, less a number held back
        
        holding:  A number of dice to hold back from rolling
        """
        return self.sOneRoll(max(self.NumDice - holding,0), self.NumSides, self.RandGen)

    def ManyRolls(self, n) :
        """
        Generates successive lists of rolled dice values
        
        n: number of rolls to generate
        """
        for i in range(n): 
            yield self.OneRoll()
        raise StopIteration

    def AllRolls(self) :
        """
        Generates all possible combinations of rolls equally weighted
        """
        return self.sAllRolls(self.NumDice, self.NumSides)

if __name__ == "__main__" :

    # Test & Demo
    dg = DiceGen(5,6)
    
    assert len(dg.OneRoll()) == 5, "failed roll length"
    assert len(dg.OneRoll(2)) == 3, "failed roll length, holding 2"
    count = 0
    for x in dg.AllRolls() :
        if x is not None: count = count + 1
    assert count == 6**5, "failed all rolls"

    print ("ok")
    