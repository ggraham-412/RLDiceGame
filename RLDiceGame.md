### RLDiceGame

#### Introduction

The code in this repository implements a simple framework for reinforced learning in dice games.
Reinforced learning refers to a machine learning framework that is able to learn from repeated 
trials.  The framework owes a lot to Markov Decision Processes: each step is described by a state
and a chosen action to be taken in that state.  The next step contains a new state calculated from
performing the action on the initial state.  Reinforced learning adds a feedback mechanism which 
allows the computed action to change in response to externally provided scores.  

Reinforced learning stands in contrast to supervised learning, which teaches a machine to classify 
states based on known classifications, and in contrast to unsupervised learning, in which a machine
identifies its own clusters in the training data.  In reinforced learning, the feedback provided is 
a score based on the initial state and action taken.  

As a particular example, a training harness is provided for a popular dice game Yamslam, by 
Blue Orange Games.  The harness and the game implement only one round of Yamslam, which comprises
an initial roll of 5 6-sided dice, a decision to keep a subset of the 5 initial dice, and re-rolling
the rest.  Each hand in Yamslam is associated with a point value, and the score of an action for a 
given original roll is simply taken to be the average increase of points from initial to final rolls.
The point values are 50 for a 5-of-a-kind, 50 for a straight of length 5, 40 for four-of-a-kind, 
30 for a full house, 25 for a flush (all evens or all odds), 20 for a straight of length 4, 10 for
three of a kind, and 5 for two pair.  Everything else is scored 0.

#### Using the code

```
python YamslamTrain.py --help
Usage: YamslamTrain.py [options]

Options:
  -h, --help            show this help message and exit
  -n NAME, --name=NAME  Name of Yamslam instance
  -t NTRAIN, --train=NTRAIN
                        Number of learning trials per roll/action
  -i INAME, --import=INAME
                        Name of game to import training from
  -p NPLAY, --play=NPLAY
                        Number of demo games to play
  -r RNAME, --rms=RNAME
                        Name of game to compare (rms) training with
  -c CNAME, --compare=CNAME
                        Name of game to compare (% agree) training with
```

#### Examples

```
#  Initially training a Yamslam game
python YamslamTrain.py -n MyYamslam -t 100 

#  Result: creates a file MyYamslam_actiontable.dat with 100 trials of directed  
#          training per roll/action combination.

#  Add to existing trainning
python YamslamTrain.py -n MyYamslam -t 100 

#  Result: loads MyYamslam_actiontable.dat, adds 100 trials of directed training 
#          per roll/action combination, and saves the result.

#  Play a few games
python YamslamTrain.py -n MyYamslam -p 5

#  Result: loads MyYamslam_actiontable.dat, plays 5 rounds of Yamslam and prints 
#          results to the console.

Initial roll: [2, 2, 2, 5, 6]
Keeping dice:  [1, 2, 3]
Final roll: [2, 2, 2, 3, 4]

Initial roll: [3, 3, 5, 5, 6]
Keeping dice:  [1, 2, 3, 4]
Final roll: [3, 3, 5, 5, 6]

Initial roll: [1, 1, 4, 5, 6]
Keeping dice:  [1, 2]
Final roll: [1, 1, 5, 5, 6]

Initial roll: [1, 2, 3, 4, 4]
Keeping dice:  [1, 2, 3, 4]
Final roll: [1, 2, 3, 4, 4]

Initial roll: [1, 4, 4, 6, 6]
Keeping dice:  [2, 3, 4, 5]
Final roll: [2, 4, 4, 6, 6]

#  Compare optimal actions to the reference set (10,000 trials of directed training
#  provided with the repository.
python YamslamTrain.py -n MyYamslam -c YamslamReference

#  Result: loads MyYamslam_actiontable.dat and the reference set, computes probability
#         that the given Yamslam games agree on optimal strategy for every unique state
0.7857142857142857
           
#  Calculate average RMS difference to the reference set (10,000 trials of directed 
#  training provided with the repository.
python YamslamTrain.py -n MyYamslam -r YamslamReference

#  Result: loads MyYamslam_actiontable.dat and the reference set, computes mean RMS
#         difference between action values for every state/action combo.
0.8117148902145583

```
