from enum import IntEnum
from DiceGen import DiceGen
from DiceGen import RollIdentifier
from RLGame import RLGame
import random
import pdb

class YamslamDiceGen(DiceGen) :
    """
    Generates rolled dice for Yamslam
    """

    NumDice = 5
    NumSides = 6
    
    def __init__(self, randGen = random.randint) :
        """
        Constructor
        
        randGen: a function that returns a random integer with same signature as
                 random.randint
        """
        super(YamslamDiceGen, self).__init__(YamslamDiceGen.NumDice, \
                                             YamslamDiceGen.NumSides, randGen)

class YamslamRolls(IntEnum) : 
    """
    Enum class to identify Yamslam rolls.  (Inherits from IntEnum so that the 
    elements are sortable.)    
    """
    Yamslam = 0
    LargeStraight = 1
    FourOfAKind = 2
    FullHouse = 3
    Flush = 4
    SmallStraight = 5
    ThreeOfAKind = 6
    TwoPair = 7
    OnePair = 8
    Bupkiss = 9
    
class YamslamRollIdentifier(RollIdentifier) :    
    """
    This class defines functions that identify patterns in rolls of 5 dice and 
    matches them to Yamslam hands.
    """                

    NumSides = 6

    # Pattern matchers
    Yamslam       = lambda counts : int(5 in counts)
    LargeStraight = lambda counts : int(counts.count(1) == 5 and \
                                       (counts[0]==0 or counts[5] == 0))
    FourOfAKind   = lambda counts : int(4 in counts or 5 in counts)
    FullHouse     = lambda counts : int(3 in counts and 2 in counts)
    Flush         = lambda counts : int((counts[0]==0 and counts[2] == 0 and counts[4]==0) or \
                                (counts[1]==0 and counts[3] == 0 and counts[5]==0))
    SmallStraight = lambda counts : int( (counts[0]>0 and counts[1] > 0 and \
                                          counts[2] > 0 and counts[3] > 0)  or \
                                         (counts[1]>0 and counts[2] > 0 and \
                                          counts[3] > 0 and counts[4] > 0)  or \
                                         (counts[2]>0 and counts[3] > 0 and \
                                          counts[4] > 0 and counts[5] > 0) )
    ThreeOfAKind  = lambda counts : int(3 in counts or 4 in counts or 5 in counts)
    TwoPair       = lambda counts : int((3 in counts and 2 in counts) or counts.count(2) == 2)
    OnePair       = lambda counts : int((2 in counts) or (3 in counts) or \
                                        (4 in counts) or (5 in counts))
    OnePairExcl   = lambda counts : int(counts.count(1)==3 and counts.count(2) == 1)
    Bupkiss       = lambda counts : int((counts.count(1) == 5) and \
                                       ((counts[2] == 0) or (counts[3] == 0)))
    
    def __init__(self) : 
        """
        Constructor
        """
        super(YamslamRollIdentifier, self).__init__(YamslamRollIdentifier.NumSides)
        self.RegisterRollIdentifier(YamslamRolls.Yamslam, YamslamRollIdentifier.Yamslam)
        self.RegisterRollIdentifier(YamslamRolls.LargeStraight, YamslamRollIdentifier.LargeStraight)
        self.RegisterRollIdentifier(YamslamRolls.FourOfAKind, YamslamRollIdentifier.FourOfAKind)
        self.RegisterRollIdentifier(YamslamRolls.FullHouse, YamslamRollIdentifier.FullHouse)
        self.RegisterRollIdentifier(YamslamRolls.Flush, YamslamRollIdentifier.Flush)
        self.RegisterRollIdentifier(YamslamRolls.SmallStraight, YamslamRollIdentifier.SmallStraight)
        self.RegisterRollIdentifier(YamslamRolls.ThreeOfAKind, YamslamRollIdentifier.ThreeOfAKind)
        self.RegisterRollIdentifier(YamslamRolls.TwoPair, YamslamRollIdentifier.TwoPair)
        self.RegisterRollIdentifier(YamslamRolls.OnePair, YamslamRollIdentifier.OnePair)
        self.RegisterRollIdentifier(YamslamRolls.Bupkiss, YamslamRollIdentifier.Bupkiss)
                            
class YamslamGame (RLGame):
    """
    Implements the dice game Yamslam.  
    
    v 1.0:  Only one round implemented, and all chips are available.      
    """

    # Dictionary of points for different Yamslam rolls
    YamslamPoints = {
        YamslamRolls.Yamslam : 50,
        YamslamRolls.LargeStraight : 50,
        YamslamRolls.FourOfAKind : 40,
        YamslamRolls.FullHouse : 30,
        YamslamRolls.Flush : 25,
        YamslamRolls.SmallStraight : 20,
        YamslamRolls.ThreeOfAKind : 10,
        YamslamRolls.TwoPair : 5,
        YamslamRolls.OnePair : 0,
        YamslamRolls.Bupkiss : 0,        
    }

    NumDice = 5
    NumSides = 6
    InitialChips = 3
    
    @staticmethod
    def StateKeyMaker(x) : 
        """Sorted list as tuple"""
        y = list(x)
        y.sort()
        return tuple(y)
        
    @staticmethod
    def ActionKeyMaker(x)  : 
        """Identity"""
        return x

    @staticmethod
    def EntryValue(x) : 
        """Returns the score of an action entry"""
        return x[2]

    @staticmethod
    def EntryCreator(*args, **kwargs) :
        """
        Creates an an action entry as a 3 element list
        
        entry[0]: sum of score improvements
        entry[1]: count of rolls trained
        entry[2]: mean score improvement per roll/action        
        """
        return [0] * 3
    
    @staticmethod
    def EntryUpdate(entry, score, *args, **kwargs) :
        """
        Updates an an action entry
        
        entry[0]: sum of score improvements
        entry[1]: count of rolls trained
        entry[2]: mean score improvement per roll/action        
        """
        entry[0] += score
        entry[1] += 1
        entry[2] = entry[0]/entry[1]
    
    @staticmethod
    def CombineEntryValue(resting_entry, incoming_entry) :
        """
        Combines incoming entry with the resting entry
        
        resting_entry: This entry will be altered to be the combination
                       of itself and the incoming entry
        incoming_entry: The entry to add to the resting_entry
        """
        resting_entry[0] = resting_entry[0] + incoming_entry[0]
        resting_entry[1] = resting_entry[1] + incoming_entry[1]
        resting_entry[2] = resting_entry[0] / resting_entry[1]
                
    def ScoreAction(self, ini_state, action, fin_state, *args, **kwargs) :
        """
        Scores the improvement of an action by taking the difference of final 
        roll value and initial roll value.
        """
        hand_ini = self.BestRoll(ini_state)
        hand_fin = self.BestRoll(fin_state)
        return YamslamGame.YamslamPoints[hand_fin] - YamslamGame.YamslamPoints[hand_ini]
    
    def __init__(self, name="YamslamGame", randGen = random.randint) : 
        """
        Constructor
        
        Initializes components:
          -RollGen:  a 5d6 dice roll generator for Yamslam 
          -RollIdentifier:  a EollIdentifier for Yamslam 
          -RollUnavailable: a map of rolls to logicals indicating if the 
              roll is available for scoring.  (See rules of Yamslam for 
              mor info.)
        """
        self.RollGen = YamslamDiceGen()
        self.RollIdentifier = YamslamRollIdentifier()
        self.RollUnavailable = {}
        for roll in YamslamRolls :
            self.RollUnavailable[roll] = False
        super(YamslamGame, self).__init__(name, YamslamGame.StateKeyMaker, \
                                                YamslamGame.ActionKeyMaker, \
                                                YamslamGame.EntryCreator, \
                                                YamslamGame.EntryValue, \
                                                YamslamGame.EntryUpdate, \
                                                YamslamGame.CombineEntryValue, \
                                                YamslamGame.ScoreAction, randGen)
                
    
    def BestRoll(self, dice) :
        """
        Returns the best matching Yamslam roll matching the dice
        
        dice:  A list of 5 die values comprising a turn in Yamslam
        """
        return self.RollIdentifier.FirstMatch(dice, self.RollUnavailable)
    
    def AllStates(self) :    
        """Returns all possible rolls in Yamslam (5d6)"""
        return self.RollGen.AllRolls()
        
    def AllActions(self) :
        """
        Returns all possible actions.
        
        An action is an integer in the closed interval [0,31].  If bit 
        i (2**i) is on, this corresponds to rolling the ith die.
        """
        return range(2**YamslamGame.NumDice)
                   
    def EvalAction(self, dice, action) : 
        """
        Evaluates an initial roll of dice against the specified action..
        
        An action is an integer in the closed interval [0,31].  If bit 
        i (2**i) is on, this corresponds to rolling the ith die.  Dice 
        indicated as being rolled will be removed from the initial roll, 
        and new dice will be rolled to replace them.  The resulting set of
        dice comprises the final roll.
        
        dice: The initial roll of 5 dice
        action: bitmask indicating which of the initial dice are to 
                be re-rolled.
        """
        newdice = []
        for i in range(YamslamGame.NumDice) :
            mask = 2 ** i
            if action & mask == 0 :
                newdice.append(dice[i])
        newdice.extend(self.RollGen.OneRoll(len(newdice)))
        newdice.sort()
        return newdice
                                    
    def ParseEntryLine(self, line) :
        """
        Parses a persisted actiontable line.
        
        line: string containing the state key, action key, and action entry
        """
        tmp = line.split(")")
        tmp1 = tmp[1].split("[")
        return eval(tmp[0]+")"), eval(tmp1[0].split(",")[1]), eval("[" + tmp1[1])
                
if __name__ == "__main__" :

    # Test and Demo
    
    ydg = YamslamDiceGen()
    assert len(ydg.OneRoll())==5, "failed, yamslam dice roll"
    
    yri = YamslamRollIdentifier()

    assert yri.FirstMatch([5,2,1,6,3])==YamslamRolls.Bupkiss, "failed, match bupkiss"
    assert yri.FirstMatch([4,2,6,2,3])==YamslamRolls.OnePair, "failed, match one pair"
    assert yri.FirstMatch([4,2,1,2,1])==YamslamRolls.TwoPair, "failed, match two pair"
    assert yri.FirstMatch([4,2,2,2,3])==YamslamRolls.ThreeOfAKind, "failed, match three of a kind"
    assert yri.FirstMatch([4,2,1,2,3])==YamslamRolls.SmallStraight, "failed, match small straight"
    assert yri.FirstMatch([4,2,6,2,4])==YamslamRolls.Flush, "failed, match flush"
    assert yri.FirstMatch([3,2,2,2,3])==YamslamRolls.FullHouse, "failed, match full house"
    assert yri.FirstMatch([4,2,2,2,2])==YamslamRolls.FourOfAKind, "failed, match four of a kind"
    assert yri.FirstMatch([4,5,1,2,3])==YamslamRolls.LargeStraight, "failed, match large straight"
    assert yri.FirstMatch([3,3,3,3,3])==YamslamRolls.Yamslam, "failed, match yamslam"
    assert yri.FirstMatch([3,3,3,3,3], {YamslamRolls.Yamslam:True})==YamslamRolls.FourOfAKind, \
        "failed, match four of a kind (yamslam)"
    all = yri.AllMatches([4,2,1,2,3])
    assert YamslamRolls.OnePair in all, "failed all match one pair"
    assert YamslamRolls.SmallStraight in all, "failed all match small straight"
    
    ygm = YamslamGame("YamslamTest")
    
    assert len(ygm.ActionTable.keys())==252, "failed action table length"
    dice = [1,3,3,4,4]
    action = 1
    newdice = ygm.EvalAction(dice, action)
    assert len(newdice) == 5, "failed eval action"
    counts = RollIdentifier.sCounts(newdice, 6)
    assert counts[2] >= 2, "failed eval action"
    assert counts[3] >= 2, "failed eval action"

    ygm.DirectedLearn([1,3,3,4,4], 1, 50)
    assert ygm.ActionTable[(1,3,3,4,4)][1][1] == 50, "failed directed learn"
    
    ygm.SaveActionTable()    
    ygm.LoadActionTable()
    ygm.ImportActionTable("YamslamTest_actiontable.dat")
    assert ygm.ActionTable[(1,3,3,4,4)][1][1] == 100, "failed import"
    
    print ("ok") 
    
