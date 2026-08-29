import sys
import time
from datetime import datetime
from Resources import *
import pygame

def touchCheck(object1, object2):
    if pygame.sprite.collide_mask(object1, object2):
        return True
    else:
        return False

def nextLevel():
    global gameMode, firstShow
    if MikeStatistics.collectedTreasure == 3:
        MikeStatistics.level += 1
        gameMode = "showLevel"
        MikeStatistics.collectedTreasure = 0
        firstShow = True
        bullets.clear()
        fishlist.clear()
        Mike.setPosition()
        gold.setPosition()
        chest.setPosition()
        sword.setPosition()
        if MikeStatistics.level == 2:
            pass


def treasureGrab(treasure):
    if Mike.iFrames == True:
        return
    if touchCheck(treasure, Mike) == True and Mike.handsFree == True:
        print("treasure")
        Mike.handsFree = False
        treasure.grabbed = True
        Mike.grabSound.play()
    if treasure.grabbed == True:
        treasure.rect.centerx = Mike.rect.centerx
        treasure.rect.y = Mike.rect.y
        if treasure.rect.y < 20:
            treasure.hide = True
            MikeStatistics.score += 50
            Mike.handsFree = True
            treasure.rect.y = -500
            treasure.grabbed = False
            Mike.swimUp.play()
            MikeStatistics.collectedTreasure += 1


def fishTouch(fish):
    if Mike.iFrames == False and touchCheck(fish, Mike) == True and fish.touching == False:
        print("fish")
        Mike.damageTaken.play()
        MikeStatistics.HP -= 1
        fish.touching = True
        Mike.iFrames = True
        Mike.iFramesTime = datetime.now().second
        Mike.handsFree = True
        if gold.grabbed == True:
            gold.grabbed = False
            gold.fall = True
        if sword.grabbed == True:
            sword.grabbed = False
            sword.fall = True
        if chest.grabbed == True:
            chest.grabbed = False
            chest.fall = True
    if touchCheck(fish, Mike) == False and fish.touching == True:
        fish.touching = False


def killFish(pulka, fish):
    if touchCheck(pulka, fish) == True:
        bullets.remove(pulka)
        fishlist.remove(fish)
        fish.fishKill.play()
        MikeStatistics.score += 10

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1300, 750))
Mike = Diver(screen)


gold = Treasure(screen, "Gold.png")
chest = Treasure(screen, "Chest.png")
sword = Treasure(screen, "Sword.png")

fishlist = []
for i in range(15):
    fish = Fish(screen)
    fishlist.append(fish)

bullets = []

MikeStatistics = Statistics(screen)
gameMode = "showLevel"
firstShow = True
startTime = None
while 1 == 1:
    screen.fill((170, 180, 220))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                Mike.moveright = True
            if event.key == pygame.K_LEFT:
                Mike.moveleft = True
            if event.key == pygame.K_UP:
                Mike.moveup = True
            if event.key == pygame.K_DOWN:
                Mike.movedown = True
            if event.key == pygame.K_SPACE:
                direction = "Left"
                if Mike.image == Mike.imageRight or Mike.image == Mike.imageTransRight:
                    direction = "Right"
                newBullet = Bullet(screen, direction, Mike.rect.centerx, Mike.rect.centery)
                bullets.append(newBullet)
                newBullet.Sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                Mike.moveright = False
            if event.key == pygame.K_LEFT:
                Mike.moveleft = False
            if event.key == pygame.K_UP:
                Mike.moveup = False
            if event.key == pygame.K_DOWN:
                Mike.movedown = False
        if event.type == pygame.QUIT:
            sys.exit()
    if gameMode == "Game":
        nextLevel()
        Mike.show()
        Mike.move()
        gold.show()
        chest.show()
        sword.show()
        treasureGrab(gold)
        treasureGrab(chest)
        treasureGrab(sword)
        MikeStatistics.showHP()
        MikeStatistics.showScore()
        for current in fishlist:
            current.show()
            current.moveX()
            current.moveY()
            fishTouch(current)
            for i in bullets:
                killFish(i, current)
        for current in bullets:
            current.show()
            current.move()
            print(len(bullets))
            if current.rect.centerx < 50 or current.rect.centerx > 1350:
                current.delete = True
            if current.delete == True:
                bullets.remove(current)
    elif gameMode == "showLevel":
        MikeStatistics.showLevel()
        if firstShow == True:
            startTime = datetime.now()
            firstShow = False
        print(datetime.now().second - startTime.second)
        if datetime.now().second - startTime.second > 2:
            gameMode = "Game"
        if startTime is None:
            pass

        elif startTime.second == 57:
            if datetime.now().second == 0:
                firstShow = False
                startTime = None
        elif startTime.second == 58:
            if datetime.now().second == 1:
                firstShow = False
                startTime = None
        elif startTime.second == 59:
            if datetime.now().second == 2:
                firstShow = False
                startTime = None


    clock.tick(100)
    pygame.display.flip()