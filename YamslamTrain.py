import random
import pdb
import os

from Yamslam import *
        
def GetYamslamRollCounts() :
    results = [0,0,0,0,0,0,0,0,0,0]
    exresults = [0,0,0,0,0,0,0,0,0,0]
    dg = YamslamDiceGen()
    for dice in dg.AllRolls():
        counts = YamslamRollIdentifier.sCounts(dice,6)
        # Non exclusive
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
            print (dice)
            
    print ("Inclusive counts:", results)
    print ("Exclusive counts:", exresults)
        
def DirectedTrain(game, num) :
    for x in game.ActionTable.keys() :
        for a in game.ActionTable[x].keys() : 
            game.DirectedLearn(x, a, num)        

def PlayGame(g, dice = None) :
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
    yg = YamslamGame("Yamslam")
    yg.LoadActionTable()
    DirectedTrain(yg, 400)
    yg.SaveActionTable()

    for i in range(10) : 
        PlayGame(yg)    
