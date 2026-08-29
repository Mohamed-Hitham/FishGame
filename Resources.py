import random

import pygame

from datetime import datetime
#добфвить на второй уровень новые рыбки и крабы
#обработать ситуации изменения game mode на game при запуске игры в 58 и 59 секунд (у дайвера подсказка)
#скачать изображение краба и рыбки для второго уровня (в лево и право)
class Treasure():
    def __init__(self, screen, img):
        self.screen = screen
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, 1250)
        self.rect.y = 625
        self.hide = False
        self.grabbed = False
        self.fall = False

    def setPosition(self):
        self.rect.x = random.randint(50, 1250)
        self.rect.y = 625
        self.hide = False

    def show(self):
        if self.hide == False:
            self.screen.blit(self.image, self.rect)
            if self.fall == True:
                if self.rect.y < 625:
                    self.rect.y += 1
                else:
                    self.fall = False

class Bullet():
    def __init__(self, screen, direction, X, Y):
        self.screen = screen
        self.image = pygame.image.load("Harpoon R.png")
        self.imageLeft = pygame.image.load("Harpoon L.png")
        self.imageRight = pygame.image.load("Harpoon R.png")
        if direction == "Left":
            self.image = self.imageLeft
        self.rect = self.image.get_rect()
        self.rect.centerx = X
        self.rect.centery = Y
        self.direction = direction
        self.Sound = pygame.mixer.Sound("Harpoon Sound.wav")
        self.speed = 5
        self.delete = False
    def move(self):
        if self.direction == "Left":
            self.rect.centerx -= self.speed
        else:
            self.rect.centerx += self.speed
    def show(self):
        self.screen.blit(self.image, self.rect)


class Fish():
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("FishL.png")
        self.imageRight = pygame.image.load("FishR.png")
        self.imageLeft = pygame.image.load("FishL.png")
        self.rect = self.image.get_rect()
        self.startposition()
        self.rect.y = random.randint(50, 650)
        self.speedx = random.randint(50, 150)/100
        self.speedy = random.randint(50, 150)/200
        self.x = self.rect.x
        self.y = self.rect.y
        self.finaleX = random.randint(0, 1300)
        self.newX = False
        self.finaleY = random.randint(50, 700)
        self.newY = False
        self.fishKill = pygame.mixer.Sound("fishKill.wav")
        self.touching = False

    def show(self):
        self.screen.blit(self.image, self.rect)

    def startposition(self):
        self.sideX = random.choice(["right", "left"])
        if self.sideX == "left":
            self.rect.centerx = random.randint(-700, 0)
            self.image = self.imageRight
        else:
            self.rect.centerx = random.randint(1300, 2000)
    def moveX(self):
        if self.newX == True:
            self.finaleX = random.randint(0, 1300)
            self.newX = False
            if self.rect.x > self.finaleX:
                self.image = self.imageLeft
            else:
                self.image = self.imageRight
        if abs(self.rect.x - self.finaleX) < 10:
            self.newX = True
        elif self.rect.x > self.finaleX:
            self.x -= self.speedx
        elif self.rect.x < self.finaleX:
            self.x += self.speedx
        self.rect.x = self.x

    def moveY(self):
        if self.newY == True:
            self.finaleY = random.randint(50, 700)
            self.newY = False
        if abs(self.rect.y - self.finaleY) < 10:
            self.newY = True
        elif self.rect.y < self.finaleY:
            self.y += self.speedy
        elif self.rect.y > self.finaleY:
            self.y -= self.speedy
        self.rect.y = self.y


class Statistics():
    def __init__(self, screen):
        self.screen = screen
        self.HP = 3
        self.level = 1
        self.score = 0
        self.imageHP = pygame.image.load("HealthHearts.png")
        self.rectHP = self.imageHP.get_rect()
        self.font = pygame.font.Font(None, 40)
        self.levelFont = pygame.font.Font(None, 200)
        self.collectedTreasure = 0

    def showHP(self):
        x = 30
        for i in range(self.HP):
            self.rectHP.x = x
            self.rectHP.y = 22
            self.screen.blit(self.imageHP, self.rectHP)
            x += 45
    def showScore(self):
        self.scoreText = self.font.render(f"score: {self.score}", True, (0, 0, 0))
        self.scoreRect = self.scoreText.get_rect()
        self.scoreRect.y = 22
        self.scoreRect.x = 1100
        self.screen.blit(self.scoreText, self.scoreRect)

    def showLevel(self):
        self.levelText = self.levelFont.render(f" LEVEL {self.level}", True, (0, 0, 0))
        self.levelRect = self.levelText.get_rect()
        self.levelRect.centery = 375
        self.levelRect.centerx = 650
        self.screen.blit(self.levelText, self.levelRect)

class Diver():
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("Diver R.png")
        self.imageRight = pygame.image.load("Diver R.png")
        self.imageLeft = pygame.image.load("Diver L.png")
        self.imageTransRight = pygame.image.load("Diver R Transparent.png")
        self.imageTransLeft = pygame.image.load("Diver L Transparent.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = 650
        self.rect.top = 15
        self.moveright = False
        self.moveleft = False
        self.moveup = False
        self.movedown = False
        self.speed = 1.2
        self.x = self.rect.centerx
        self.y = self.rect.y
        self.handsFree = True
        self.grabSound = pygame.mixer.Sound("Grab.wav")
        self.swimUp = pygame.mixer.Sound("Surface.wav")
        self.damageTaken = pygame.mixer.Sound("DamageSound.wav")
        self.iFrames = False
        self.iFramesTime = None
    def move(self):
        if self.moveright == True:
            if self.image != self.imageRight:
                self.image = self.imageRight
            if self.rect.left > 1270:
                self.rect.right = 40
                self.x = self.rect.x
            self.x += self.speed
        if self.moveleft == True:
            if self.image != self.imageLeft:
                self.image = self.imageLeft
            if self.rect.right < 30:
                self.rect.left = 1260
                self.x = self.rect.x
            self.x -= self.speed
        if self.movedown == True:
            self.y += self.speed
        if self.moveup == True:
            self.y -= self.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def setPosition(self):
        self.rect.centerx = 650
        self.rect.top = 15

    def show(self):
        self.stopiFrames()
        self.imageChange()
        self.screen.blit(self.image, self.rect)

    def imageChange(self):
        if self.iFrames == True:
            if self.image == self.imageRight:
                self.image = self.imageTransRight
            elif self.image == self.imageLeft:
                self.image = self.imageTransLeft
        else:
            if self.image == self.imageTransRight:
                self.image = self.imageRight
            elif self.image == self.imageTransLeft:
                self.image = self.imageLeft

    def stopiFrames(self):
        if self.iFramesTime is None:
            return
        if self.iFramesTime < 57:
            if datetime.now().second > self.iFramesTime+2:
                self.iFrames = False
                self.iFramesTime = None
        elif self.iFramesTime == 57:
            if datetime.now().second == 0:
                self.iFrames = False
                self.iFramesTime = None
        elif self.iFramesTime == 58:
            if datetime.now().second == 1:
                self.iFrames = False
                self.iFramesTime = None
        elif self.iFramesTime == 59:
            if datetime.now().second == 2:
                self.iFrames = False
                self.iFramesTime = None