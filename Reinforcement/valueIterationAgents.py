# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        states = self.mdp.getStates()

        "iterate for defined ammount of iterations"
        for iteration in range(self.iterations):
            "temp variable to hold predecessor states"
            predecessors = util.Counter()

            "loop through all states to update values"
            for state in states:
                maxValue = float('-inf')
                actions = self.mdp.getPossibleActions(state)
                "loop through all possible actions from current state"
                for possibleAction in actions:
                    value = 0
                    "get next state a probability of going there"
                    for nextState, probability in self.mdp.getTransitionStatesAndProbs(state, possibleAction):
                        """ update the value to be the sum of each nextStates 
                        prob * (reward + (discount * value)) """
                        value += probability * (self.mdp.getReward(state, possibleAction, nextState) + 
                        self.discount * self.values[nextState])
                    maxValue = max(maxValue, value)
                
                "update predecessors"
                if maxValue != float('-inf'):
                    predecessors[state] = maxValue
            
            "update all state values for next iteration"
            for state in states: 
                self.values[state] = predecessors[state]


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        
        qValue = 0
        "get state and probls, then calculate q"
        for nextState, probability in self.mdp.getTransitionStatesAndProbs(state, action):
            "reward"
            reward = self.mdp.getReward(state, action, nextState)
            "formula from slides"
            qValue += probability * (reward + (self.discount * self.getValue(nextState)))
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        "check for terminal state"
        if self.mdp.isTerminal(state):
            return None

        "variable to calculate best action"
        best = float('-inf')
        bestAction = None
        "loop through each action and find highest qVal, update best action"
        for possibleAction in self.mdp.getPossibleActions(state):
            value = self.computeQValueFromValues(state, possibleAction)
            "new highest q value"
            if value > best:
                best = value
                "reassign best action"
                bestAction = possibleAction
        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        states = self.mdp.getStates()
        numStates = len(states)

        for iteration in range(self.iterations):
            "allows for one state per iteration"
            state = states[iteration % numStates]
            "check for terminal state"
            if not self.mdp.isTerminal(state):
                
                actions = self.mdp.getPossibleActions(state)
                value = float('-inf')
                for action in actions: 
                    if self.getQValue(state, action) > value:
                        value = self.getQValue(state, action)
                self.values[state] = value         
            
class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        "set to hold predecessors"
        predecessors = {}
        "priority queue to prioritize value iteration"
        fringe = util.PriorityQueue()

        "find all the predecessors"
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                "get all possible actions"
                for possibleAction in self.mdp.getPossibleActions(state):
                    "find next states and probabilities"
                    for nextState, probability in self.mdp.getTransitionStatesAndProbs(state, possibleAction):
                        """if next state is in predecessors: add current state, 
                        else: next state already in predecessors"""
                        if nextState in predecessors:
                            predecessors[nextState].add(state)
                        else:
                            predecessors[nextState] = {state}
    
        "For each non terminal state"
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                "find the highest Q values for all possible actions"
                highestQ = float('-inf')
                for action in self.mdp.getPossibleActions(state):
                    if self.computeQValueFromValues(state, action) > highestQ:
                        highestQ = self.computeQValueFromValues(state, action)
                "set diff and update fringe"
                diff = abs(self.values[state] - highestQ)
                """pQueues update will handle updates of the heap and check if state
                is already in the heap with different value"""
                fringe.update(state, -diff)

        "iterate for designated # of iterations"
        for iteration in range(self.iterations):
            "if fringe is empty, terminate"
            if fringe.isEmpty():
                break
            "pop off front element: desired priority state"
            state = fringe.pop()

            "if state isn't terminal, find highest Qvalue and update current states value"
            if not self.mdp.isTerminal(state):
                maxQ = float('-inf')
                for action in self.mdp.getPossibleActions(state):
                    if self.computeQValueFromValues(state, action) > maxQ:
                        maxQ = self.computeQValueFromValues(state, action)
                self.values[state] = maxQ
            
            "for each predecessor of the current state"
            for predecessor in predecessors[state]:
                """if the predecessor isn't terminal: find highest Qvalue and push the predecessor 
                with highestQ"""
                if not self.mdp.isTerminal(predecessor):
                    biggestQ = float('-inf')
                    for action in self.mdp.getPossibleActions(predecessor):
                        if self.computeQValueFromValues(predecessor, action) > biggestQ:
                            biggestQ = self.computeQValueFromValues(predecessor, action)
                    diff = abs(self.values[predecessor] - biggestQ)
                    
                    if diff > self.theta:
                        """pQueues update will handle updates of the heap and check if predecessor
                        is already in the heap with different value"""
                        fringe.update(predecessor, -diff)

