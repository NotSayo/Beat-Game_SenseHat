import time
from sense_hat import *
import random

#region classes

class Game():
    bricks = []
    lives = 5
    score = 0


    def AddBrick(self, Brick):
        self.bricks.insert(len(self.bricks), Brick)

    def RemoveBrick(self, index):
        self.bricks.pop(index)

    def GetBricks(self):
        return self.bricks
    
    def RemoveLife(self):
        self.lives -= 1

    def GetLives(self):
        return self.lives
    def AddPoints(self, points):
        self.score += points
    
    def GetScore(self):
        return self.score


class Brick():
    moveSpeed = 50

    position = []
    extraPosition = []
    site = ''
    color = ''
    moveTimer = 0

    def __init__(self, site, color):
        self.site = site
        self.color = color

    def GetSite(self):
        return self.site
        
    def GetPosition(self):
        return self.position
    
    def GetExtraPosition(self):
        return self.extraPosition
    
    def GetColor(self):
        return self.color
    
    def ChangeSpeed(self, newValue):
        self.moveSpeed = newValue
    
    def GetMoveSpeed(self):
        return self.moveSpeed
    
    def UpdatePosition(self, position = []):
        self.position = position

    def CheckMove(self):
        if self.moveTimer == self.moveSpeed:
            self.moveTimer = 0
            self.UpdatePosition()
        else:
            self.moveTimer += 1

    def DefineStartingPosition(self):
        if self.site == 'l':
            self.position = [0,3]
            self.extraPosition = [0,4]
        elif self.site == 'u':
            self.position = [3,0]
            self.extraPosition = [4,0]
        elif self.site == 'r':
            self.position = [7,3]
            self.extraPosition = [7,4]
        elif self.site == 'd':
            self.position = [3,7]
            self.extraPosition = [4,7]

    def UpdatePosition(self):
        if self.site == 'l':
            self.position[0] += 1
            self.extraPosition[0] += 1
        elif self.site == 'u':
            self.position[1] += 1
            self.extraPosition[1] += 1
        elif self.site == 'r':
            self.position[0] -= 1
            self.extraPosition[0] -= 1
        elif self.site == 'd':
            self.position[1] -= 1
            self.extraPosition[1] -= 1
    


    

#endregion


#region colors

p =  [ 20,20,255 ] # light blue / player
w = [ 255,255,255 ] # white
r = [ 204,0,0 ]  # red
pu = [ 127,0,255 ] # purple
pi = [ 255,0,255 ] # pink
g = [ 0,204,102 ] # green
y = [ 255,255,0 ] # yellow

#endregion

#region Global Variables

sense = SenseHat()
game = Game()

board = [
    w,w,w,w,w,w,w,w,
    w,w,w,w,w,w,w,w,
    w,w,w,w,w,w,w,w,
    w,w,w,p,p,w,w,w,
    w,w,w,p,p,w,w,w,
    w,w,w,w,w,w,w,w,
    w,w,w,w,w,w,w,w,
    w,w,w,w,w,w,w,w,
]

sites = [ 'l', 'u', 'r', 'd'] # left, up, right, down
colors = [ r, pu, pi, g, y]

ConstSpawnFreq = 50
spawnFreq = 0
nextIncrease = 2

#endregion

#region Board

def AddToBoard(b, position, extraPosition, color):
    positionIndex = 8 * position[1] + position[0]
    extraPositionIndex = 8 * extraPosition[1] + extraPosition[0]

    b[positionIndex] = color
    b[extraPositionIndex] = color
    return b

#endregion

#region Bricks

def GenerateBrick():
    global game

    number = random.randint(0,3)
    site = sites[number]
    number = random.randint(0, len(colors) - 1)
    color = colors[number]

    brick = Brick(site, color)
    brick.DefineStartingPosition()
    game.AddBrick(brick)

def DisplayBricks():
    b = []
    for i in range(len(board)):
        b.append(board[i])

    bricks = game.GetBricks()
    try:
        for i in range(len(bricks) + 1):
                position = bricks[i].GetPosition()
                extraPosition = bricks[i].GetExtraPosition()
                color = bricks[i].GetColor()
                b = AddToBoard(b, position, extraPosition, color)

    except:
        pass

    finally:
        return b
        
def CheckMoveBricks():
    bricks = game.GetBricks()
    for i in range(len(bricks)):
        bricks[i].CheckMove()

def CheckMiddleBrick():
    bricks = game.GetBricks()
    try:
        for i in range(len(bricks)):
            position = bricks[i].GetPosition()
            if position == [3,3] or position == [3,4] or position == [4,3] or position == [4,4]:
                game.RemoveLife()
                game.RemoveBrick(i)
    except:
        pass


def CheckSpeedIncrease():
    global spawnFreq
    global nextIncrease
    score = game.GetScore

    if (score == nextIncrease):
        nextIncrease *= 2
        spawnFreq *= 0.2
        bricks = game.GetBricks()

        for i in range(len(bricks)):
            bricks[i].ChangeSpeed(bricks[i].GetMoveSpeed() * 0.2)




#endregion

#region User Input

def Hit(direction):
    global game

    if direction == 'left':
        position1 = [2,3]
        position2 = [2,4]
    elif direction == 'up':
        position1 = [3,2]
        position2 = [4,2]
    elif direction == 'right':
        position1 = [5,3]
        position2 = [5,4]
    elif direction == 'down':
        position1 = [3,5]
        position2 = [4,5]
    
    bricks = game.GetBricks()
    try:
        hit = False
        for i in range(len(bricks)):
            if bricks[i].GetPosition() == position1 or bricks[i].GetPosition() == position2:
                game.AddPoints(1)
                game.RemoveBrick(i)
                hit = True
    except:
        pass
    if not hit:
        game.RemoveLife()

#endregion
            
#region Lifes

def CheckIfDead():
    lifes = game.GetLives()

    return lifes == 0

def EndScreen():
    score = game.GetScore()
    sense.clear()
    sense.show_message("Game Over",0.08,w)
    sense.show_message("Score: " +  str(score), 0.08, w)


#endregion

#region Game

def GameLoop():
    global moveFreq
    global spawnFreq
    
    while(True):
        # Input Check

        for event in sense.stick.get_events():
            if (event.action == ACTION_PRESSED):
                Hit(event.direction)

        # Spawn & Move

        if spawnFreq == ConstSpawnFreq:
            spawnFreq = 0
            GenerateBrick()
        else:
            spawnFreq += 1

        CheckMoveBricks()
        CheckMiddleBrick()

        CheckSpeedIncrease()

        # Lifes

        if(CheckIfDead()):
            EndScreen()
            return
            
        #Display

        b = DisplayBricks()
        sense.clear()
        sense.set_pixels(b)

        time.sleep(0.02)


GameLoop()

#endregion




