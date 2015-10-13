import random
import os

from Yamslam import *
        
def GetYamslamRollCounts() :
    """
    This function analyzes all possible rolls of Yamslam and counts frequencies of
    each roll pattern.  Counts are analyzed inclusively (ie- a Five of a Kind is also a 
    Four of a Kind, etc) and exclusively (ie- a Five of a Kind is counted separately
    from Four of a Kind)    
    """
    results = [0,0,0,0,0,0,0,0,0,0]
    exresults = [0,0,0,0,0,0,0,0,0,0]
    dg = YamslamDiceGen()
    for dice in dg.AllRolls():
        counts = YamslamRollIdentifier.sCounts(dice,6)

        # Inlusive
        results[0] = results[0] + YamslamRollIdentifier.Yamslam(counts)
        results[1] = results[1] + YamslamRollIdentifier.LargeStraight(counts)
        results[2] = results[2] + YamslamRollIdentifier.FourOfAKind(counts)
        results[3] = results[3] + YamslamRollIdentifier.FullHouse(counts)
        results[4] = results[4] + YamslamRollIdentifier.Flush(counts)
        results[5] = results[5] + YamslamRollIdentifier.SmallStraight(counts)
        results[6] = results[6] + YamslamRollIdentifier.ThreeOfAKind(counts)
        results[7] = results[7] + YamslamRollIdentifier.TwoPair(counts)
        results[8] = results[8] + YamslamRollIdentifier.OnePair(counts)
        results[9] = results[9] + YamslamRollIdentifier.Bupkiss(counts)

        # Exclusive
        if YamslamRollIdentifier.Yamslam(counts) == 1 : 
            exresults[0] = exresults[0] + 1            
        elif YamslamRollIdentifier.LargeStraight(counts) :
            exresults[1] = exresults[1] + 1
        elif YamslamRollIdentifier.FourOfAKind(counts) :
            exresults[2] = exresults[2] + 1
        elif YamslamRollIdentifier.FullHouse(counts) :
            exresults[3] = exresults[3] + 1
        elif YamslamRollIdentifier.Flush(counts) :
            exresults[4] = exresults[4] + 1
        elif YamslamRollIdentifier.SmallStraight(counts) :
            exresults[5] = exresults[5] + 1
        elif YamslamRollIdentifier.ThreeOfAKind(counts) :
            exresults[6] = exresults[6] + 1
        elif YamslamRollIdentifier.TwoPair(counts) :
            exresults[7] = exresults[7] + 1
        elif YamslamRollIdentifier.OnePair(counts) :
            exresults[8] = exresults[8] + 1
        elif YamslamRollIdentifier.Bupkiss(counts) :
            exresults[9] = exresults[9] + 1
        else :
            print ("Unknown: ", dice)
            
    print ("Inclusive counts:", results)
    print ("Exclusive counts:", exresults)
        
def DirectedTrain(game, num=1) :
    """
    Does directed training on the game.  This enumerates over all possible 
    keys and actions and executed num instances of training.  If the training 
    model is deterministic in initial_state and action, then num = 1 may be 
    used.  If the model is random in initial_state and action, then num should 
    be > 1.
    
    game: an instance of RLGame
    num: number of trials for each initial state and action.
    """
    for x in game.ActionTable.keys() :
        for a in game.ActionTable[x].keys() : 
            for i in range(num) :
                newdice = game.EvalAction(x, a)
                game.Learn(x, a, newdice)

def RMS_ActionTable(game1, game2) :
    """
    Calculates the RMS difference between the ActionTable values of Yamslam game1 
    and game2.  
    """    
    
    sum = 0
    count = 0
    for x in game1.ActionTable.keys():
        for a in game1.ActionTable[x].keys():
            count = count + 1
            sum = sum + (game1.ActionTable[x][a][2] - game2.ActionTable[x][a][2])**2
    return (sum/count)**(0.5)
                
def PlayGame(g, dice = None) :
    """
    This method plays one round of Yamslam and prints the results to the 
    screen
    
    g:  An instance of YamslamGame
    dice:  The initial roll can be set to see how the game responds to a particular 
           roll.  If not given a roll is generated randomly.
    """    
    if dice is None :
        dice = g.RollGen.OneRoll()
    print ("Initial roll:", dice)
    action = g.GetAction(dice, 0)
    keepers = []
    for i in range(YamslamGame.NumDice) :
        mask = 2 ** i
        if action & mask == 0 :
            keepers.append(i+1)            
    print ("Keeping dice: ", keepers)
    newdice = g.EvalAction(dice, action)
    print ("Final roll:", newdice)
    
    
        
if __name__ == "__main__" :

    #GetYamslamRollCounts()
#    yg1 = YamslamGame("Yamslam1")
#    yg1.LoadActionTable()
#    yg2 = YamslamGame("Yamslam2")
#    yg2.LoadActionTable()
    yg3 = YamslamGame("Yamslam3")
    yg3.LoadActionTable()
    yg4 = YamslamGame("Yamslam4")
    DirectedTrain(yg4, 20)
    rms = RMS_ActionTable(yg4,yg3)
    print (rms)

