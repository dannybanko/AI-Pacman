# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    """ the discount with no noise will encourage pacman to go towards the 10
    because the action of going east will always happen"""
    answerDiscount = 0.9
    answerNoise = 0.0
    return answerDiscount, answerNoise

def question3a():
    """ The discount with no noise and no living reward will encourage pacman 
    to take the cliff path because there is no noise, and go to the 1.0 reward
    because the discount wouldn't be worth it for 10""" 
    answerDiscount = .25
    answerNoise = 0
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    """Discount and noise encourages pacman to go to exit 1.0 and avoid the cliff
    because there is a chance of ending up in the -10 and the discout makes the 
    +10 no longer worth it """
    answerDiscount = 0.3
    answerNoise = 0.3
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    """No noise a closer to 1 discount makes pacman take the cliff to the 10
    because east will go east 100% of the time and the reward is greater at 10 """
    answerDiscount = .7
    answerNoise = 0
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    """ the 1 discount and the noise encourages pacman to go the the 10 while
    not risking the cliff because the noise could make pacman get -10.0 but 
    the discount is high enough to make pacman prefer the 10 reward"""
    answerDiscount = 1
    answerNoise = 0.5
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e(): 
    """ providing a living reward and no discount encourages pacman to avoid
    exiting at the 1.0 and 10.0 because pacman would recieve infinite living 
    reward """ 
    answerDiscount = 1
    answerNoise = 0
    answerLivingReward = 5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question8():
    answerEpsilon = None
    answerLearningRate = None
    return 'NOT POSSIBLE'
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
