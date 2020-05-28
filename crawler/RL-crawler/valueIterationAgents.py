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
        
        # initialize the value function for all states
        states = self.mdp.getStates()
            
        # run iterations of updating the value function
        for i in range(self.iterations):
            # save a temporary copy of the values
            v = util.Counter()
            for state in states:
                if not self.mdp.isTerminal(state):
                    action = self.getAction(state)
                    v[state] = self.computeQValueFromValues(state, action)
                    
            self.values = v


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
        # util.raiseNotDefined()
        
        # sum up all of the transition values for this action
        value = 0
        for nextState, probs in self.mdp.getTransitionStatesAndProbs(state, action):
            reward = self.mdp.getReward(state, action, nextState)
            value += probs * (reward + self.discount*self.getValue(nextState))
            
        return value


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        
        # get a list of possible actions
        actions = self.mdp.getPossibleActions(state)
        if not actions:
            return None

        max_value = None
        best_action = None
        
        for action in actions:
            
            value = self.computeQValueFromValues(state, action)
            # update best action and max value
            if max_value is None or value > max_value:
                best_action = action
                max_value = value

        return best_action
        

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
        # initialize the value function for all states
        states = self.mdp.getStates()
        for state in states:
            self.values[state] = 0
            
        # run iterations of updating the value function
        for i in range(self.iterations):

            # round robin through the states during iterations
            state = states[i % len(states)]
            if not self.mdp.isTerminal(state):
                action = self.getAction(state)
                self.values[state] = self.computeQValueFromValues(state, action)
        

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
        
        """
            build a list of state predecessors using a dictionary
            with the key=state and item=set of predecesor states
        """
        states = self.mdp.getStates()
        predecessors = {}
        
        for state in states:
            if not self.mdp.isTerminal(state):
                for action in self.mdp.getPossibleActions(state):
                    for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                        if nextState in predecessors:
                            predecessors[nextState].add(state)
                        else:
                            predecessors[nextState] = {state}

        """
            build a priority queue of states based upon the largest difference 
            between current and stored value
        """
        pq = util.PriorityQueue()
        
        for state in states:
            if not self.mdp.isTerminal(state):
                action = self.getAction(state)
                diff = abs(self.computeQValueFromValues(state, action) - self.values[state])
                pq.update(state, - diff)
                
        """
            iteration:
                take top state from queue and update its value
                since this affects the values of all predecessors of this state,
                calculate the value difference for each predecessor
                if this exceeds a threshold theta, then update the queue with this predecessor
        """
        
        for i in range(self.iterations):
            if pq.isEmpty():
                break
            
            state = pq.pop()
            if not self.mdp.isTerminal(state):
                action = self.getAction(state)
                self.values[state] = self.computeQValueFromValues(state, action)
                
                
            for pred_state in predecessors[state]:
                if not self.mdp.isTerminal(pred_state):
                    action = self.getAction(pred_state)
                    diff = abs(self.computeQValueFromValues(pred_state, action) - self.values[pred_state])
                
                    if diff > self.theta:
                        pq.update(pred_state, -diff)

