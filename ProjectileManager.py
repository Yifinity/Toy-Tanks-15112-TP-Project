# Class the manages all the projectiles that are in the game
# Should have permissions to remove projectiles, and call kill functions
from cmu_graphics import *
from Enemies.GreenEnemy import * 
from Enemies.YellowEnemy import *
from Enemies.RedEnemy import * 

import random

class ProjectileManager:
    def __init__(self, app):
        self.objects = app.objects

        # Other classes will add to this list
        self.projectiles = []
        self.stepCount = 0
        self.secCount = 2.5

        self.tankQueue = []

    def addMissile(self, missile):
        self.projectiles.append(missile)

    def onStep(self, app):
        self.stepCount += 1
        if self.stepCount / 60 >= self.secCount:
            self.generateNextTank()
            self.stepCount = 0

        # First check that it's not empty
        for projectile in self.projectiles: 
            if projectile.checkCollision(app): 
                for object in self.objects:
                    # Check collision of targets
                    check = object.checkHit(projectile)
                    
                    if check: # if we haven't hit an enemy
                        # Check if we hit grid/or out of bounds
                        projectile.onStep()
                    
                    else:
                        if object == app.user:
                            app.gameOver = True
                        else:
                            app.userScore += 1
                            self.addNextTank(object)

                        self.projectiles.remove(projectile)
                        return
            else:
                # If we fail the grid-boundary test
                self.projectiles.remove(projectile)
                return


    def redraw(self, app):
        for projectile in self.projectiles:
            projectile.drawProjectile(app)

    def addNextTank(self, enemy):
        selection = random.randint(0, 2)
        if selection == 0:
            self.tankQueue.append(GreenEnemy(enemy.x, enemy.y))
        elif selection == 1:
            self.tankQueue.append(YellowEnemy(enemy.x, enemy.y))
        else:
            self.tankQueue.append(RedEnemy(enemy.x, enemy.y))
        
        self.objects.remove(enemy)



    # Remove the enemy and add a new one
    def generateNextTank(self):
        self.objects.append(self.tankQueue[0])
        self.tankQueue.pop(0)

