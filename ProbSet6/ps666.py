import math
import random

import ps6_visualize
import pylab

class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getTile(self):
        return str([int(self.x), int(self.y)])
    def getNewPosition(self, angle, speed):
        old_x, old_y = self.getX(), self.getY()
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

class RectangularRoom(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = {}
        for w in range(width):
            for h in range(height):
                self.tiles[str([w,h])] = False

    def cleanTile(self, pos):
        self.tiles[pos.getTile()] = True

    def isTileCleaned(self, width, height):
        return self.tiles[str([width, height])]

    def getNumTiles(self):
        return self.width * self.height

    def getNumCleanedTiles(self):
        clean = 0
        for w in range(self.width):
            for h in range(self.height):
                if self.tiles[str([w,h])]:
                    clean += 1
        return clean

    def getRandomPosition(self):
        return Position(self.width * random.random(), self.height * random.random())

    def isPositionInRoom(self, pos):
        return pos.x >= 0.0 and pos.y >= 0.0 \
               and pos.x <= self.width and pos.y <= self.height

class Robot(object):
    def __init__(self, room, speed):
        self.room = room
        self.speed = speed
        self.pos = self.room.getRandomPosition()
        self.direction = 359.49 * random.random()
        self.room.cleanTile(self.pos)

    def getRobotPosition(self):
        return self.pos

    def getRobotDirection(self):
        return self.direction

    def setRobotPosition(self, position):
        self.pos = position

    def setRobotDirection(self, direction):
        self.direction = direction

    def setRandDirection(self):
        self.direction = int(random.random() * 359.499)

    def wallReset(self):
        if self.pos.x < 0.0:
            self.pos.x = 0.0
        elif self.pos.y < 0.0:
            self.pos.y = 0.0
        elif self.pos.x > self.room.width:
            self.pos.x = self.room.width
        elif self.pos.y > self.room.height:
            self.pos.y = self.room.height

    def updatePositionAndClean(self):
        self.pos = self.pos.getNewPosition(self.direction, self.speed)
        if not self.room.isPositionInRoom(self.pos):
            self.wallReset()
##            self.setRobotDirection(35
        self.room.tiles[self.pos.getTile()] = True

class StandardRobot(Robot):
        def updatePositionAndClean(self):
            self.pos = self.pos.getNewPosition(self.direction, self.speed)
            if not self.room.isPositionInRoom(self.pos):
                self.wallReset()
                self.setRandDirection()
            self.room.tiles[self.pos.getTile()] = True

class RandomWalkRobot(Robot):
    def updatePositionAndClean(self):
        self.setRandDirection()
        self.pos = self.pos.getNewPosition(self.direction, self.speed)
        if not self.room.isPositionInRoom(self.pos):
            self.wallReset()
        self.room.tiles[self.pos.getTile()] = True
        

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
        compiled, results = [], 0
        if min_coverage > 1:
            min_coverage = min_coverage / 100.0
        for t in range(num_trials):
##            anim = ps6_visualize.RobotVisualization(num_robots, width, height)
            ticker = 0
            room = RectangularRoom(width, height)
            complete = min_coverage * room.getNumTiles()
            robots = []
            for i in range(num_robots):
                robots += [robot_type(room, speed)]
            while room.getNumCleanedTiles() < complete:
                for r in robots:
                    r.updatePositionAndClean()
                ticker += 1
##                anim.update(room, robots)
            compiled += [ticker]
##            anim.done()
        for i in compiled:
            results += i
        results = results/float(num_trials)
        return round(results)

# == Problem 4

def showPlot1(numTrials):
## time to clean 80% of 20x20 with per 1-10 robots
## time on y-axis, robots on XXX
    yTime, xBots = [], []
    for i in range(1, 11):
       yTime += [runSimulation(i, 1, 20, 20, .8, numTrials, StandardRobot)]
       xBots += [i]
    pylab.plot(xBots, yTime)
    pylab.title('Time required to clean 80% of a 20x20 room')
    pylab.xlabel('Number of Standard Robots')
    pylab.ylabel('Time in seconds')
    pylab.show()

def showPlot2(numTrials):
## cleaning time per room shape
    yTime, xRatio = [], []
    rooms = [[20, 20], [25,16], [40,10], [50,8], [80,5], [100,4]]
    for i in rooms:
        xRatio.append(i[0]/ i[1])
        yTime.append(runSimulation(2, 1, i[0], i[1], .8, numTrials, StandardRobot))
    pylab.plot(xRatio, yTime, 'ro')
    pylab.title('Time for two StandardRobots to clean 80% of rooms based by \
ratio of long edge to short')
    pylab.xlabel('Ratio of length to width')
    pylab.ylabel('Time required to clean room')
    pylab.show()

def showPlot3(numTrials):
    robotics, results = [StandardRobot, RandomWalkRobot], []
    xBots = [1,2,3,4,5,6,7,8,9,10]
    for r in robotics:
        for i in range(1, 11):
            results.append(runSimulation(i, 1, 20, 20, .8, numTrials, r))
    yStandard = results[0:10]
    yRandom = results[10:20]
    pylab.plot(xBots[:], yStandard, 'g-', label='Standard')
    pylab.plot(xBots[:], yRandom, 'r-', label='Random')
    pylab.title('Standard Robots vs. Random Robots in 20x20 rooms')
    pylab.xlabel('Number of robots')
    pylab.ylabel('Time to clean room')
    pylab.show()

##   The Standard Robot consistently outperforms the RandomWalk in every instance.
##
##   Originally I thought the Random might do better; that maybe iRobot knew this
## but stuck with Standard programming because an unpredictable Roomba might
## scare consumers. This theory was disproven.
