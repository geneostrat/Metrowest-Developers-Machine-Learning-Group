# crawler.py
# ----------
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


#!/usr/bin/python
import math
from math import pi as PI
import environment

class CrawlingRobotEnvironment(environment.Environment):

    def __init__(self, crawlingRobot):

        self.crawlingRobot = crawlingRobot

        # The state is of the form (armAngle, handAngle)
        # where the angles are bucket numbers, not actual
        # degree measurements
        self.state = None

        self.nArmStates = 9
        self.nHandStates = 13

        # create a list of arm buckets and hand buckets to
        # discretize the state space
        minArmAngle,maxArmAngle = self.crawlingRobot.getMinAndMaxArmAngles()
        minHandAngle,maxHandAngle = self.crawlingRobot.getMinAndMaxHandAngles()
        armIncrement = (maxArmAngle - minArmAngle) / (self.nArmStates-1)
        handIncrement = (maxHandAngle - minHandAngle) / (self.nHandStates-1)
        self.armBuckets = [minArmAngle+(armIncrement*i) \
           for i in range(self.nArmStates)]
        self.handBuckets = [minHandAngle+(handIncrement*i) \
         for i in range(self.nHandStates)]

        # Reset
        self.reset()

    def getCurrentState(self):
        """
          Return the current state
          of the crawling robot
        """
        return self.state

    def getPossibleActions(self, state):
        """
          Returns possible actions
          for the states in the
          current state
        """

        actions = list()

        currArmBucket,currHandBucket = state
        if currArmBucket > 0: actions.append('arm-down')
        if currArmBucket < self.nArmStates-1: actions.append('arm-up')
        if currHandBucket > 0: actions.append('hand-down')
        if currHandBucket < self.nHandStates-1: actions.append('hand-up')

        return actions

    def doAction(self, action):
        """
          Perform the action and update
          the current state of the Environment
          and return the reward for the
          current state, the next state
          and the taken action.

          Returns:
            nextState, reward
        """
        nextState, reward =  None, None

        oldX = self.crawlingRobot.getRobotPosition()

        armBucket,handBucket = self.state
        armAngle,handAngle = self.crawlingRobot.getAngles()
        if action == 'arm-up':
            newArmAngle = self.armBuckets[armBucket+1]
            self.crawlingRobot.moveArm(newArmAngle)
            nextState = (armBucket+1,handBucket)
        if action == 'arm-down':
            newArmAngle = self.armBuckets[armBucket-1]
            self.crawlingRobot.moveArm(newArmAngle)
            nextState = (armBucket-1,handBucket)
        if action == 'hand-up':
            newHandAngle = self.handBuckets[handBucket+1]
            self.crawlingRobot.moveHand(newHandAngle)
            nextState = (armBucket,handBucket+1)
        if action == 'hand-down':
            newHandAngle = self.handBuckets[handBucket-1]
            self.crawlingRobot.moveHand(newHandAngle)
            nextState = (armBucket,handBucket-1)

        newX = self.crawlingRobot.getRobotPosition()
        railFlags = self.crawlingRobot.getRailFlags()

        # a simple reward function
        reward = newX - oldX

        self.state = nextState
        return nextState, reward, railFlags


    def reset(self):
        """
         Resets the Environment to the initial state
        """
        ## Initialize the state to be the middle
        ## value for each parameter e.g. if there are 13 and 19
        ## buckets for the arm and hand parameters, then the intial
        ## state should be (6,9)
        ##
        ## Also call self.crawlingRobot.setAngles()
        ## to the initial arm and hand angle

        armState = self.nArmStates//2
        handState = self.nHandStates//2
        self.state = armState,handState
        self.crawlingRobot.setAngles(self.armBuckets[armState],self.handBuckets[handState])
        self.crawlingRobot.positions = [self.crawlingRobot.getRobotPosition()]


class CrawlingRobot:

    def __init__(self):

        ## Arm and Hand Degrees ##
        self.armAngle = self.oldArmDegree = 0.0
        self.handAngle = self.oldHandDegree = -PI/6

        self.maxArmAngle = PI/2
        self.minArmAngle = 0

        self.maxHandAngle = 0
        self.minHandAngle = -PI/2


        ## Robot Body ##
        self.robotWidth = 30
        self.robotHeight = 20
        self.robotPos = 20
        
        self.minRailPos = 10
        self.maxRailPos = 110

        ## Robot Arm ##
        self.armLength = 50

        ## Robot Hand ##
        self.handLength = 60

        self.positions = [20]


    def setAngles(self, armAngle, handAngle):
        """
            set the robot's arm and hand angles
            to the passed in values
        """
        self.armAngle = armAngle
        self.handAngle = handAngle

    def getAngles(self):
        """
            returns the pair of (armAngle, handAngle)
        """
        return self.armAngle, self.handAngle

    def getRobotPosition(self):
        """
            returns the (x,y) coordinates
            of the lower-left point of the
            robot
        """
        return self.robotPos

    def getRailFlags(self):
        """
            returns flags indicating whether robot is outside of
            safe travel region
        """
        xPos = self.getRobotPosition()
        
        return {'Min' : xPos < self.minRailPos, 
                'Max' : xPos > self.maxRailPos}

    def moveArm(self, newArmAngle):
        """
            move the robot arm to 'newArmAngle'
        """
        if newArmAngle > self.maxArmAngle:
            raise Exception('Crawling Robot: Arm Raised too high. Careful!')
        if newArmAngle < self.minArmAngle:
            raise Exception('Crawling Robot: Arm Raised too low. Careful!')
        disp = self.displacement(self.armAngle, self.handAngle,
                                  newArmAngle, self.handAngle)
        curXPos = self.robotPos
        self.robotPos = curXPos+disp
        self.armAngle = newArmAngle

        # Position and Velocity Sign Post
        self.positions.append(self.getRobotPosition())
        if len(self.positions) > 100:
            self.positions.pop(0)

    def moveHand(self, newHandAngle):
        """
            move the robot hand to 'newArmAngle'
        """

        if newHandAngle > self.maxHandAngle:
            raise Exception('Crawling Robot: Hand Raised too high. Careful!')
        if newHandAngle < self.minHandAngle:
            raise Exception('Crawling Robot: Hand Raised too low. Careful!')
        disp = self.displacement(self.armAngle, self.handAngle, self.armAngle, newHandAngle)
        curXPos = self.robotPos
        self.robotPos = curXPos+disp
        self.handAngle = newHandAngle

        # Position and Velocity Sign Post
        self.positions.append(self.getRobotPosition())
        if len(self.positions) > 100:
            self.positions.pop(0)


    def getMinAndMaxArmAngles(self):
        """
            get the lower- and upper- bound
            for the arm angles returns (min,max) pair
        """
        return self.minArmAngle, self.maxArmAngle


    def getMinAndMaxHandAngles(self):
        """
            get the lower- and upper- bound
            for the hand angles returns (min,max) pair
        """
        return self.minHandAngle, self.maxHandAngle


    def getRotationAngle(self):
        """
            get the current angle the
            robot body is rotated off the ground
        """
        armCos, armSin = self.__getCosAndSin(self.armAngle)
        handCos, handSin = self.__getCosAndSin(self.handAngle)
        x = self.armLength * armCos + self.handLength * handCos + self.robotWidth
        y = self.armLength * armSin + self.handLength * handSin + self.robotHeight
        if y < 0:
            return math.atan(-y/x)
        return 0.0


    ## You shouldn't need methods below here


    def __getCosAndSin(self, angle):
        return math.cos(angle), math.sin(angle)

    def displacement(self, oldArmDegree, oldHandDegree, armDegree, handDegree):

        oldArmCos, oldArmSin = self.__getCosAndSin(oldArmDegree)
        armCos, armSin = self.__getCosAndSin(armDegree)
        oldHandCos, oldHandSin = self.__getCosAndSin(oldHandDegree)
        handCos, handSin = self.__getCosAndSin(handDegree)

        xOld = self.armLength * oldArmCos + self.handLength * oldHandCos + self.robotWidth
        yOld = self.armLength * oldArmSin + self.handLength * oldHandSin + self.robotHeight

        x = self.armLength * armCos + self.handLength * handCos + self.robotWidth
        y = self.armLength * armSin + self.handLength * handSin + self.robotHeight

        if y < 0:
            if yOld <= 0:
                return math.sqrt(xOld*xOld + yOld*yOld) - math.sqrt(x*x + y*y)
            return (xOld - yOld*(x-xOld) / (y - yOld)) - math.sqrt(x*x + y*y)
        else:
            if yOld  >= 0:
                return 0.0
            return -(x - y * (xOld-x)/(yOld-y)) + math.sqrt(xOld*xOld + yOld*yOld)

        raise Exception('Never Should See This!')

