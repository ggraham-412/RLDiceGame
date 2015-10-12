import random
import os
import os.path
import pdb

class RLGame (object):
    
    def __init__(self, name,        \
                       sKeyMaker,   \
                       aKeyMaker,   \
                       entryCreate, \
                       entryValue,  \
                       entryUpdate, \
                       scoreAction, \
                       randGen = random.randint) : 
        self.InitializeActionTable() 
        self.Name = name
        self.StateKeyMaker = sKeyMaker
        self.ActionKeyMaker = aKeyMaker
        self.EntryCreator = entryCreate   
        self.GetEntryValue = entryValue
        self.UpdateEntryValue = entryUpdate
        self.RandGen = randGen

    def InitializeActionTable(self, *args, **kwargs) :
        self.ActionTable = {}
        for state in self.AllStates() :
            func = self.StateKeyMaker
            skey = func(state)
            self.ActionTable[skey] = {}
            for action in self.AllActions() : 
                akey = (self.ActionKeyMaker)(action)
                self.ActionTable[skey][akey] = (self.EntryCreator)(*args, **kwargs)

    def ScoreAction(self, ini_state, action, fin_state, *args, **kwargs) :
        raise NotImplementedError("Not implemented")

    def AllStates(self) :
        raise NotImplementedError("Not implemented")

    def AllActions(self, state = None) :
        raise NotImplementedError("Not implemented")

    def EvalAction(self, state, action) : 
         raise NotImplementedError("Not implemented")
                               
    def Learn(self, ini_state, action, fin_state, *args, **kwargs) :
        score = self.ScoreAction(ini_state, action, fin_state, *args, **kwargs)
        skey = self.StateKeyMaker(ini_state)
        akey = self.ActionKeyMaker(action)
        self.UpdateEntryValue(self.ActionTable[skey][akey], score, *args, **kwargs)
        
    def GetAction(self, state, tolerance, *args, **kwargs) :
        possibleActions = []
        if tolerance < 0 : 
            possibleActions.extend(self.AllActions(state))
        else :
            maxval = 0
            skey = self.StateKeyMaker(state)
            for action in self.AllActions() :
                akey = self.ActionKeyMaker(action)
                val = self.GetEntryValue(self.ActionTable[skey][akey])
                if ( val > maxval ) :
                    maxval = val
            for action in self.AllActions() :
                akey = self.ActionKeyMaker(action)
                val = self.GetEntryValue(self.ActionTable[skey][akey])
                if ( maxval - val ) <= tolerance : 
                    possibleActions.append(action)
        idx = self.RandGen(0,len(possibleActions)-1)
        return possibleActions[idx]
                       
    def DirectedLearn(self, state, action, numtry) :    
        for i in range(numtry) :
            newstate = self.EvalAction(state, action)
            self.Learn(state, action, newstate)
            
    def MakeFilename(self, what) :
        return self.Name + "_" + what + ".dat"    
           
    def SaveActionTable(self) :        
        file = open(self.MakeFilename("actiontable"),"w")
        for skey in self.ActionTable.keys() :
            for akey in self.ActionTable[skey].keys() :
                entry = self.ActionTable[skey][akey]
                file.write(repr(skey))
                file.write(',')
                file.write(repr(akey))
                file.write(',')
                file.write(repr(entry))
                file.write("\n")
        file.close()

    def ParseEntryLine(line) :
        raise NotImplementedError("Not Implemented")
        
    def LoadActionTable(self) :
        filename = self.MakeFilename("actiontable")
        if not os.path.exists(filename) :
            return
        self.InitializeActionTable()
        file = open(filename,"r")
        for line in file.readlines() :
            skey, akey, entry = self.ParseEntryLine(line)
            self.ActionTable[skey][akey] = entry
        file.close()
                
        
        

    