import pygame, time, sys, random, math
from operator import itemgetter
from pygame.locals import *
pygame.init()

class GameLoop(object):
    def __init__(self):
        pygame.init()

        WINDOW_WIDTH = 1000
        WINDOW_HEIGHT = 1000

        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),0,32)
        pygame.display.set_caption("Space Invaders")
        self.delay = 0 #HOW FAST PROGRAM RUNS

    def generateEnemies(self, enemyList):
        enemies = []
        counter = 0
        for i in enemyList:
            counter2 = 0
            counter += 1
            for o in i:
                pos = ((counter2+1)*70,(counter+1)*70)
                if o == 1:
                    x = Enemy(pos, self.surface, self.sataliteList)
                elif o == 2:
                    x = Enemy2(pos, self.surface, self.sataliteList)
                elif o == 3:
                    x = Enemy3(pos, self.surface, self.sataliteList)
                enemies.append(x)
                counter2 += 1
        return enemies
        
    def generateSatalite(self):#stephen's Stuff

        for i in range (4):
            satalite=Satalite((i*283,700))
            self.sataliteList.append(satalite)
            self.surface.blit(satalite.image,satalite.rect)

    def drawSatalite(self):
        for i in self.sataliteList:
            if i.health == 4:
                i.image = pygame.image.load("barrierHitOne.png")
                i.image = pygame.transform.scale(i.image, (150,150))
            if i.health == 3:
                i.image = pygame.image.load("barrierHitTwo.png")
                i.image = pygame.transform.scale(i.image, (150,150))
            if i.health == 2:
                i.image = pygame.image.load("barrierHitThree.png")
                i.image = pygame.transform.scale(i.image, (150,150))
            if i.health == 1:
                i.image = pygame.image.load("barrierHitFour.png")
                i.image = pygame.transform.scale(i.image, (150,150))
            if i.health <= 0:
                self.sataliteList.remove(i)
            
            self.surface.blit(i.image,i.rect)
            
    def moveEnemies(self):
        for i in self.enemies:
            if Enemy.changeDir == True:
                for g in self.enemies:
                    g.changeDirection()
                    self.surface.blit (g.image, g.rect)
                Enemy.changeDir = False
                break
            elif Enemy.downCount != 0 and Enemy.downCount != 1:
                for x in self.enemies:
                    x.moveDown()
                    self.surface.blit (x.image, x.rect)
                Enemy.downCount -= 1
                break
            elif Enemy.downCount == 1:
                for x in self.enemies:
                    x.moveDown()
                    self.surface.blit (x.image, x.rect)
                Enemy.changeDir = True
                Enemy.downCount -= 1
                break
            elif i.getRight() > 950 and Enemy.downCount == 0 or i.getLeft() < 50 and Enemy.downCount == 0:
                Enemy.downCount = 50
                break
            i.move()
            self.surface.blit (i.image, i.rect)

    def shipReg(self):
        for i in self.enemies:
            if i.rect.colliderect(self.spaceship.rect):
                self.lives = 0
                
    def enemyFire(self):
        enemy = random.randint(0,len(self.enemies)-1)
        self.enemies[enemy].fire()
    
    def excecute(self):
        wave1 = [[1,1,1,1],[1,1,1,1]]
        wave2 = [[1,1,1,1],[2,2,2,2]]
        wave3 = [[1,1,1,1],[2,2,2,2], [3,3,3,3]]
        
        bg = pygame.image.load("bgtemp.png")
        bg = pygame.transform.scale(bg, (1000,1000))
        bgRect = bg.get_rect()
        bgRect.topleft = (0,0)
        self.enemies = []
        font = pygame.font.SysFont('', 30)
        #STEVEN STUFF
        self.sataliteList = []
        self.generateSatalite()
        #//
        self.lives = 3
        wavecounter = 1
        loopcounter = 1
        while True:
            if self.enemies == []:
                if wavecounter == 1:
                    self.enemies = self.generateEnemies(wave1)
                    self.spaceship = Spaceship(self.surface, self.enemies, 0, (500,875), self.sataliteList)
                elif wavecounter == 2:
                    self.generateSatalite()
                    self.enemies = self.generateEnemies(wave2)
                    self.spaceship = Spaceship(self.surface, self.enemies, self.spaceship.score, self.spaceship.rect.topleft, self.sataliteList)
                elif wavecounter == 3:
                    self.generateSatalite()
                    self.enemies = self.generateEnemies(wave3)
                    self.spaceship = Spaceship(self.surface, self.enemies, self.spaceship.score, self.spaceship.rect.topleft, self.sataliteList)
                else:
                    self.generateSatalite()
                    self.enemies = self.generateEnemies(wave3)
                    self.spaceship = Spaceship(self.surface, self.enemies, self.spaceship.score, self.spaceship.rect.topleft, self.sataliteList)
                wavecounter += 1
            if self.lives == 0:
                self.surface.blit(font.render("Lives: "  + str(self.lives), True, (0, 0, 0)), (800, 50))
                print(self.spaceship.score)
                return self.spaceship.score
                break
            self.surface.blit(bg,bgRect)
            self.moveEnemies()
            self.surface.blit(font.render("Wave: "  + str(wavecounter-1), True, (255, 255, 255)), (450, 50))
            self.surface.blit(font.render("Score: "  + str(self.spaceship.score), True, (255, 255, 255)), (100, 50))
            self.surface.blit(font.render("Lives: "  + str(self.lives), True, (255, 255, 255)), (800, 50))
            #STEVEN STUFF
            self.spaceship.handle_keys() # controls keys
            self.spaceship.draw()
            self.drawSatalite()
            #//
            #Bullet Handling
            self.spaceship.moveShots()
            if loopcounter == 50: #ENEMY FIRE RATE
                self.enemyFire()
                loopcounter = 1
            for i in self.enemies:
                i.moveBullets()
                if i.bullet.colliderect(self.spaceship):
                    i.draw = False
                    i.bullet.center = (i.rect.center[0],i.rect.bottom)
                    self.lives -= 1
            #//
            self.shipReg()
            pygame.display.update()
            time.sleep (self.delay)
            loopcounter += 1

    
class Enemy(object):
    changeDir = False
    downCount = 0
    bulletSpeed = 4
    def __init__(self, initPos, surface, sataliteList):
        self.sataliteList = sataliteList
        self.image = pygame.image.load("enemy1.png")
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.topleft = initPos
        self.speed = 2 #USE FOR HORIZONTAL SPEED
        self.y = 2 #USE FOR VERTICAL SPEED
        self.health = 1 #USE FOR ENEMY HEALTH
        self.score = 5 #USE FOR ENEMY SCORE
        self.surface = surface
        self.bulletImg = pygame.image.load("enemybullet.png")
        self.bulletImg = pygame.transform.scale(self.bulletImg, (10,25))
        self.bullet = self.bulletImg.get_rect()
        self.bullet.center = (self.rect.center[0],self.rect.bottom)
        self.draw = False

    def fire(self):
        if self.draw == False:
            self.bullet.center = (self.rect.center[0],self.rect.bottom)
            self.surface.blit(self.bulletImg,self.bullet)
            self.draw = True

    def moveBullets(self):
        if self.draw == True:
            for i in self.sataliteList:
                if i.rect.colliderect(self.bullet):
                    self.draw = False
                    self.bullet.center = (self.rect.center[0],self.rect.bottom)
                    i.health -= 1
            if self.bullet.top > 1000:
                self.draw = False
            else:
                self.bullet.move_ip(0, self.bulletSpeed)
                self.surface.blit(self.bulletImg,self.bullet)

    def move(self):
        self.rect.move_ip(self.speed, 0)

    def changeDirection(self):
        self.speed = -self.speed
        self.rect.move_ip(self.speed, 0)

    def moveDown(self):
        self.rect.move_ip(0, self.y)

    def getRight(self):
        return self.rect.right
    
    def getLeft(self):
        return self.rect.left

class Enemy2(Enemy):
    def __init__(self, initPos, surface, sataliteList):
        self.sataliteList = sataliteList
        self.image = pygame.image.load("enemy2.png")
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.topleft = initPos
        self.speed = 2 #USE FOR HORIZONTAL SPEED
        self.y = 2 #USE FOR VERTICAL SPEED
        self.health = 2 #USE FOR ENEMY HEALTH
        self.score = 10 #USE FOR ENEMY SCORE
        self.surface = surface
        self.bulletImg = pygame.image.load("enemybullet.png")
        self.bulletImg = pygame.transform.scale(self.bulletImg, (10,25))
        self.bullet = self.bulletImg.get_rect()
        self.bullet.center = (self.rect.center[0],self.rect.bottom)
        self.draw = False

class Enemy3(Enemy):
    def __init__(self, initPos, surface, sataliteList):
        self.sataliteList = sataliteList
        self.image = pygame.image.load("enemy3.png")
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.topleft = initPos
        self.speed = 2 #USE FOR HORIZONTAL SPEED
        self.y = 2 #USE FOR VERTICAL SPEED
        self.health = 2 #USE FOR ENEMY HEALTH
        self.score = 20 #USE FOR ENEMY SCORE
        self.surface = surface
        self.bulletImg = pygame.image.load("enemybullet.png")
        self.bulletImg = pygame.transform.scale(self.bulletImg, (10,25))
        self.bullet = self.bulletImg.get_rect()
        self.bullet.center = (self.rect.center[0],self.rect.bottom)
        self.draw = False


class Spaceship(object):  # represents the bird, not the game
    def __init__(self, surface, enemies, score, position, sataliteList):
        self.sataliteList = sataliteList
        self.enemies = enemies
        self.surface = surface
        self.position = position
        self.score = score
        """ The constructor of the class """
        self.image = pygame.image.load("images.jpg")
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position[0], self.position[1])
        # the spaceships' position
        self.shots = []
        self.bulletSpeed = 4 #how fast the bullets move
        self.lastShot = 0
        self.shotDelay = 0.5 #time in seconds between shots


    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 4 # distance moved in 1 frame, try changing it to 5

        if key[pygame.K_RIGHT]: # right key
            self.rect.move_ip(dist,0) # move right
            if self.rect.right>=1000:#scale value to size of spaceship
                self.rect.move_ip(-dist,0)
        elif key[pygame.K_LEFT]: # left key
            self.rect.move_ip(-dist,0) # move left
            if self.rect.left<0:
                self.rect.move_ip(dist,0)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    if pygame.time.get_ticks()/1000 - self.lastShot/1000 > self.shotDelay:
                        self.fire()
                        self.lastShot = pygame.time.get_ticks()

    def draw(self):
        """ Draw on surface """
        # blit yourself at your current position
        self.surface.blit(self.image, self.rect)

    def moveShots(self):
        for i in self.shots:
            for satalite in self.sataliteList:
                if i.colliderect(satalite):
                    try:
                        self.shots.remove(i)
                    except:
                        pass
                    satalite.health -= 1
                    
            for x in self.enemies:
                if i.colliderect(x):
                    try:
                        self.shots.remove(i)
                    except:
                        pass
                    x.health -= 1
                    if x.health == 0:
                        self.enemies.remove(x)
                    self.score += x.score
            if i.bottom < 0:
                self.shots.remove(i)
            else:
                i.move_ip(0, -self.bulletSpeed)
                self.surface.blit(self.bullet,i)
    
    def fire(self):
        self.bullet = pygame.image.load("bullet.png")
        self.bullet = pygame.transform.scale(self.bullet, (10,25))
        imageRect = self.bullet.get_rect()
        imageRect.center = (self.rect.center[0],self.rect.top)
        self.surface.blit(self.bullet,imageRect)
        self.shots.append(imageRect)

class Satalite(object):#Stephen's Stuff
    def __init__(self,initPos):
        """ The constructor of the class """
         #call Sprite initalizer
        self.image = pygame.image.load("barrier.png")
        self.image = pygame.transform.scale(self.image, (150,150))
        # the spaceships' position
        self.rect = self.image.get_rect()
        self.rect.topleft = initPos
        self.health=5

class Menu (object) :
    def __init__ (self) :
        # Creates fonts
        self.font = pygame.font.SysFont ('', 36)
        self.fontLead = pygame.font.SysFont ('', 50)
        self.fontTitle = pygame.font.SysFont ('', 70)
        # creates timing
        self.clock = pygame.time.Clock()
        self.fps = 60
        # creates window specifications
        self.size = [800, 600]
        self.bg = [0, 0, 0]
        # creates screen
        self.screen = pygame.display.set_mode (self.size)
        self.screen.fill (self.bg)
        # creates asteroid move amounts
        self.X_MOVE_AMT = 2
        self.angle = 0
        # creates leaderboard list
        self.leaders = []

    def start (self):
        # creates asteroid
        asteroid = pygame.image.load ("asteroidIntro.png")
        asteroid = pygame.transform.scale (asteroid, (75, 75))
        asteroidRect = asteroid.get_rect (center = (75/2, 75/2))
        self.screen = pygame.display.set_mode (self.size)
        asteroidRect.topleft = (0, 200)
        self.bg = [0,0,0]
        end = True
        while end :
            # Spins asteroid
            self.angle += 0.25
            self.angle %= 360
            asteroidSpin = pygame.transform.rotate (asteroid, self.angle)
            # Moves asteroid
            asteroidRect.left += self.X_MOVE_AMT
            self.screen.blit (asteroidSpin, asteroidRect)
            # Creates buttons
            buttonStart = pygame.Rect (300, 400, 200, 50) # Creates start button
            buttonLead = pygame.Rect (300, 475, 200, 50) # Creates leaderboard button
            # Draws buttons
            pygame.draw.rect (self.screen, [0, 255, 0], buttonStart) 
            pygame.draw.rect (self.screen, [0, 255, 0], buttonLead) 
            # Draws text
            self.screen.blit (self.fontTitle.render("Welcome to Space Invaders!", True, (0, 255, 0)), (75, 100))
            self.screen.blit (self.font.render('Click to Start', True, (0, 0, 0)), (325, 415))
            self.screen.blit (self.font.render('Leaderboards', True, (0, 0, 0)), (320, 490))

            # Updates screen
            pygame.display.update ()
            self.clock.tick (self.fps)
            self.screen.fill (self.bg)

            if asteroidRect.right > self.size [0] + 240 :
                asteroidRect.left = -241

            for event in pygame.event.get ():
                if event.type == pygame.QUIT:
                    pygame.quit ()
                    sys.exit ()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if buttonLead.collidepoint(mouse_pos):
                        # prints current location of mouse
                        self.outputLead ()
                        end = False
                    if buttonStart.collidepoint(mouse_pos):
                        # prints current location of mouse
                        self.explain ()
                        end = False

    def explain (self) :
        self.bg = [255, 255, 255]
        self.screen.fill (self.bg)
        # Creates and draws fonts
        self.fontTitle = pygame.font.SysFont ('', 70)
        self.screen.blit (self.fontTitle.render("Rules Of The Game:", True, (0, 0, 0)), (165, 100))
        self.screen.blit (self.font.render ("Use left and right arrows to move around", True, (0, 0, 0)), (160, 155))
        self.screen.blit (self.font.render ("Use spacebar to shoot at the aliens", True, (0, 0, 0)), (195, 190))
        self.screen.blit (self.font.render ("Don't let the aliens reach you!", True, (0, 0, 0)), (220, 225))
        self.screen.blit (self.fontLead.render ("Click Anywhere to Continue", True, (0, 0, 0)), (175, 500))

        # Creates alien image
        alien = pygame.image.load ("alien_face.png")
        alien = pygame.transform.scale (alien, (150, 150))
        alienRect = alien.get_rect ()
        alienRect.topleft = (325, 300)
        # Updates screen
        self.screen.blit (alien, alienRect)
        pygame.display.update ()
        while True :
            for event in pygame.event.get () :
                if event.type == pygame.QUIT:
                    pygame.quit ()
                    sys.exit ()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = GameLoop()
                    score = x.excecute()
                    self.gameOver = pygame.font.SysFont ('', 90)
                    self.screen.fill ([255, 255, 255])
                    self.screen.blit (self.gameOver.render("GAME OVER", True, (0, 0, 0)), (320, 400))
                    pygame.display.update ()
                    time.sleep(4)
                    self.inputLead (score) # receives score

    def readLead (self) :
        self.leaders = []
        snIn = open ("Leaderboard.txt", "r")
        while True : # Reads info from text file
            info = {}
            info ["Name"] = str.strip (snIn.readline ())
            if info ["Name"] == "" :
                break
            info ["Score"] = int(str.strip (snIn.readline ()))
            self.leaders.append (info)
        print (self.leaders)
        snIn.close ()

    def outputLead (self) :
        self.readLead ()
        self.bg = [0, 0, 0]
        self.screen.fill (self.bg)
        sortedLead = sorted (self.leaders, key = itemgetter ("Score")) # Sorts list
        height = 70
        count = 0

        self.screen.blit (self.fontTitle.render ("High Scores", True, (0, 255, 0)), (100, 50))
        for elem in reversed (sortedLead) :
            height += 30 # Moves the info down each time
            count += 1
            self.screen.blit (self.fontLead.render (str (count) + ".   ", True, (0, 255, 0)), (100, height))
            self.screen.blit (self.fontLead.render (elem ["Name"], True, (0, 255, 0)), (175, height))
            self.screen.blit (self.fontLead.render (str (elem ["Score"]), True, (0, 255, 0)), (400, height))
            pygame.display.update ()
            if count == 10 : # Iterates through 10 times
                break

        end = True
        while end :
            buttonReturn = pygame.Rect (300, 430, 200, 50) # Creates return button
            pygame.draw.rect (self.screen, [0, 255, 0], buttonReturn) 
            self.screen.blit (self.font.render('Back to Start', True, (0, 0, 0)), (325, 445))
            pygame.display.update ()

            for event in pygame.event.get ():
                if event.type == pygame.QUIT:
                    pygame.quit ()
                    sys.exit ()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if buttonReturn.collidepoint (mouse_pos) :
                        # finds current location of mouse
                        self.start ()
                        end = False

    def inputLead (self, score) :
        self.bg = [0, 0, 0]
        self.screen.fill (self.bg)

        # Inputs the info for the current user and adds it to a text file
        snOut = open ("Leaderboard.txt", "a")
        name = ""
        font = pygame.font.Font (None, 50)
        end = True
        while end :
            for evt in pygame.event.get() :
                if evt.type == KEYDOWN :
                    if evt.unicode.isalpha () :
                        name += evt.unicode
                    elif evt.key == K_BACKSPACE :
                        name = name[:-1]
                    elif evt.key == K_RETURN :
                        # Ends loop and adds info to text file
                        end = False
                        snOut.write (name + "\n")
                        snOut.write (str (score) + "\n")
                        snOut.close ()
                        # Restarts opening screen
                        self.start ()
            # Outputs current inputted name
            self.screen.fill (self.bg)
            self.screen.blit (self.fontTitle.render('Please enter your name:', True, (0, 255, 0)), (100, 100))
            block = font.render(name, True, (0, 255, 0))
            rect = block.get_rect()
            rect.center = self.screen.get_rect().center
            self.screen.blit(block, rect)
            pygame.display.flip()

x = Menu ()
x.start ()
