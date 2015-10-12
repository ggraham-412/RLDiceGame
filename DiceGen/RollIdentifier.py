class RollIdentifier(object):
    """
    Identifies a roll of dice according to a pattern
    """

    @staticmethod
    def sCounts(dice, maxNumber) :
        """
        Transforms a roll of dice into list of frequencies of occurrences of each 
        distinct number appearing in the roll
        
        dice: list of dice 
        maxNumber: the maximum number that can apear on the dice
        """
        rtv = [0] * maxNumber
        for d in dice :
            rtv[d-1] = rtv[d-1] + 1
        return rtv  
        
    def __init__(self, numSides) :
        """
        Constructor
        
        numSides: number of sides per die
        """
        self.RollIdentifiers = {}
        self.NumSides = numSides
        
    def RegisterRollIdentifier(self, rollKey, func) :
        """
        Registers an external function that identifies dice rolls
        
        rollKey: A unique, sortable object that identifies a specific 
                 roll pattern
        func: takes a list of frequencies of distinct numbers in a roll of 
              dice, and returns 1 if the roll matches the dice or 0 otherwise
        """
        self.RollIdentifiers[rollKey] = func
        
    def FirstMatch(self, dice, skips={}) :
        """
        Returns the roll that is the first match among the ordered set of roll
        identifiers
        
        dice:  List of rolled dice
        skips:  a dictionary of roll identifiers to hold out of the search
        """
        counts = self.sCounts(dice, self.NumSides)
        for roll in sorted(self.RollIdentifiers) :
            if skips.get(roll, False) : 
                continue
            if self.RollIdentifiers[roll](counts) :
                return roll
        return None                
            
    def AllMatches(self, dice) :
        """
        Returns all rolls that match the dice
        
        dice:  List of rolled dice
        skips:  a dictionary of roll identifiers to hold out of the search
        """
        rtv = []
        counts = self.sCounts(dice, self.NumSides)
        for roll in self.RollIdentifiers :
            if self.RollIdentifiers[roll](counts) :
                rtv.append(roll)
        return rtv
            
if __name__ == "__main__" :

    # Test and Demo
    counts = RollIdentifier.sCounts([1,4,2,3,3,5,5,5], 6)
    assert counts[0] == 1, "failed counts - 1"
    assert counts[1] == 1, "failed counts - 2"
    assert counts[2] == 2, "failed counts - 3"
    assert counts[3] == 1, "failed counts - 4"
    assert counts[4] == 3, "failed counts - 5"
    assert counts[5] == 0, "failed counts - 6"

    ri = RollIdentifier(6)
    
    ri.RegisterRollIdentifier(1, lambda x: int(x[0] == 1))
    ri.RegisterRollIdentifier(2, lambda x: int(x[1] == 2))
    ri.RegisterRollIdentifier(3, lambda x: int(x[2] == 3))
    ri.RegisterRollIdentifier(4, lambda x: int(x[3] == 4))
    ri.RegisterRollIdentifier(5, lambda x: int(x[4] == 5))
    
    assert ri.FirstMatch([4,2,5,1,3])==1, "failed, first match 1"
    assert ri.FirstMatch([4,2,5,2,3])==2, "failed, first match 2"
    assert ri.FirstMatch([4,3,5,3,3])==3, "failed, first match 3"
    assert ri.FirstMatch([4,4,4,2,4])==4, "failed, first match 4"
    assert ri.FirstMatch([5,5,5,5,5])==5, "failed, first match 5"
    assert ri.FirstMatch([5,5,2,5,5]) is None, "failed, no match"
    assert ri.FirstMatch([5,5,1,5,5], {1:True}) is None, "failed, no match skip 1"

    matches = ri.AllMatches([2,2,3,3,3])
    assert 2 in matches, "failed, multimatch 2"
    assert 3 in matches, "failed, multimatch 3"
        
    print("ok")

