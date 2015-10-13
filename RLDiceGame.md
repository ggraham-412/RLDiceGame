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

# Train a Uamslam game a

