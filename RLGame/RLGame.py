import random
import os
import os.path
import pdb

class RLGame (object):
    """
    Class represents a simple one step, re-inforced learning game
    
    Components include  
        -Name which identifies the game instance. 
        -ActionTable which maps game states and actions to an 
         action table entry that scores the actions, 
        -methods to compute keys to the action table from states and actions 
        -methods to manage action table entries
        -a method to score a particular action.  The scoring function may be 
         deterministic (supervised learning) or stochastic (reinforcement learning).
    """
    def __init__(self, name,        \
                       sKeyMaker,   \
                       aKeyMaker,   \
                       entryCreate, \
                       entryValue,  \
                       entryUpdate, \
                       entryCombine,\
                       scoreAction, \
                       randGen = random.randint) : 
        self.InitializeActionTable() 
        self.Name = name
        self.StateKeyMaker = sKeyMaker
        self.ActionKeyMaker = aKeyMaker
        self.EntryCreator = entryCreate   
        self.GetEntryValue = entryValue
        self.UpdateEntryValue = entryUpdate
        self.CombineEntryValue = entryCombine
        self.RandGen = randGen

    def InitializeActionTable(self, *args, **kwargs) :
        """
        Enumerates all possible states and actions, and initializes 
        the action table entries
        """
        self.ActionTable = {}
        for state in self.AllStates() :
            func = self.StateKeyMaker
            skey = func(state)
            self.ActionTable[skey] = {}
            for action in self.AllActions() : 
                akey = (self.ActionKeyMaker)(action)
                self.ActionTable[skey][akey] = (self.EntryCreator)(*args, **kwargs)

                               
    def Learn(self, ini_state, action, fin_state, *args, **kwargs) :
        """
        Based on a calculated or (randomly) generated score, updates the 
        action table entry corresponding to the given initial state and action
        
        ini_state: Initial game state
        action: Action taken
        fin_state: Final game state
        """
        score = self.ScoreAction(ini_state, action, fin_state, *args, **kwargs)
        skey = self.StateKeyMaker(ini_state)
        akey = self.ActionKeyMaker(action)
        self.UpdateEntryValue(self.ActionTable[skey][akey], score, *args, **kwargs)
        
    def GetAction(self, state, tolerance, *args, **kwargs) :
        """
        Given an initial state, returns the action which maximizes the  
        expected return in the final state
        
        tolerance:  A parameter to allow some slippage in the maximum value.
            == 0:  No slippage.  An action will be chosen randomly from a set of 
                   actions whichequal the maxmimum return
             > 0:  An action will be chosen randomly from a set of actions which 
                   have a return within tolerance of the maximum
             < 1:  Exploration mode: an action will be chosen randomly from 
                   the set of all possible actions.             
        """
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
                       
    def DirectedLearn(self, state, action, numtry=1) :    
        """
        For a given state and action, directs the game to teach itself 
        the consequences of its action.  For a supervied learning problem
        with deterministic outcomes, numtry should be 1.  For a problem
        with random outcomes, numtry should be high enough to gather enough 
        data.
        
        state: The state of the game to train on
        action: The action to learn on
        numtry: Number of times to 
        """
        for i in range(numtry) :
            newstate = self.EvalAction(state, action)
            self.Learn(state, action, newstate)
                       
    def MakeFilename(self, what) :
        """
        Makes a filename for persistence of game data
        """
        return self.Name + "_" + what + ".dat"    

    def SaveActionTable(self) :        
        """
        Saves the contents of the action table to a file.
        """
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

    def ImportActionTable(self, fromfile) :        
        """
        Imports the contents of the given file and combines with the 
        existing action table.  (Take care not to import the same data 
        more than once!)
        """
        if not os.path.exists(fromfile) :
            return
        file = open(filename,"r")
        for line in file.readlines() :
            skey, akey, entry = self.ParseEntryLine(line)
            self.CombineEntryValue(self.ActionTable[skey][akey], entry)
        file.close()

    def LoadActionTable(self) :
        """
        Loads the contents of the action table from a file.
        """
        filename = self.MakeFilename("actiontable")
        if not os.path.exists(filename) :
            print ("Warning in game " + self.Name + ": Could not load action table from " + filename)
            return
        self.InitializeActionTable()
        file = open(filename,"r")
        for line in file.readlines() :
            skey, akey, entry = self.ParseEntryLine(line)
            self.ActionTable[skey][akey] = entry
        file.close()

    # To be implemented by subclass
        
    def ScoreAction(self, ini_state, action, fin_state, *args, **kwargs) :
        """
        Returns a score for an action that starts from ini_state and ends in fin_state.
        
        ini_state: The initial state of the game
        action: The action taken
        fin_state: The final state resulting from ini_state and action
        """
        raise NotImplementedError("Not implemented")

    def AllStates(self) :
        """
        Generator of all possible states in the game, for use in generating keys
        for the action table.  
        
        This is applicable to a finite dice game where the states are discrete and 
        enumerable.  For a continuous domain problem, a set of points that covers the 
        state space may be used instead.  
        """
        raise NotImplementedError("Not implemented")

    def AllActions(self, state = None) :
        """
        Generator of all possible actions in the game, for use in generating keys for 
        the action table.  
        
        This is applicable to a finite dice game where the actions are discrete and 
        enumerable.  For a continuous domain problem, a set of points that covers the 
        action space may be used instead.  
        """
        raise NotImplementedError("Not implemented")

    def EvalAction(self, state, action) : 
        """
        Evaluates the action against the given state and returns a new state.  
        For example, in a dice game the initial state may be a set of rolled dice,
        and the action may be a directive to hold some dice and re-roll the others. 
        
        state:  The initial state
        action:  An action to be taken against the initial state.
        """
        raise NotImplementedError("Not implemented")

    def ParseEntryLine(line) :
        """
        Parses a persisted actiontable line.
        
        line: string containing the state key, action key, and action entry
        """
        raise NotImplementedError("Not Implemented")
        
        
        

    