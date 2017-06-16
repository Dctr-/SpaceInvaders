import pygame, time, sys, random, math, os
from operator import itemgetter
from pygame.locals import *
pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (15,30) #Place window properly


class GameLoop(object):
    def __init__(self):
        pygame.init() #initialize python

        WINDOW_WIDTH = 1000 #set window specs
        WINDOW_HEIGHT = 1000

        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),0,32) #create surface
        pygame.display.set_caption("Space Invaders") #caption it
        self.delay = 0 #Global delay

    def generateEnemies(self, enemyList): #generates enemies on screen, 2d array passed in
        enemies = []
        counter = 0
        for i in enemyList: #loop through 2d array
            counter2 = 0
            counter += 1
            for o in i: 
                pos = ((counter2+1)*70,(counter+1)*70) #place them in rows on screen
                if o == 1:
                    x = Enemy(pos, self.surface, self.sataliteList) #enemy1
                elif o == 2:
                    x = Enemy2(pos, self.surface, self.sataliteList) #enemy2
                elif o == 3:
                    x = Enemy3(pos, self.surface, self.sataliteList) #enemy3
                enemies.append(x) #enemy types are specified by an integer and interpreted here, appended to a list
                counter2 += 1
        return enemies #return the list of enemies
        
    def generateSatalite(self):#Generate a satalite

        for i in range (4): #generate 4 satalites at fixed positions, add them to a list
            satalite=Satalite((i*283,700))
            self.sataliteList.append(satalite)
            self.surface.blit(satalite.image,satalite.rect)

    def drawSatalite(self): #draw the satalites
        for i in self.sataliteList:
            if i.health == 4: #handle health by swapping images
                i.image = pygame.image.load("barrierHitOne.png")
                i.image = pygame.transform.scale(i.image, (150,150)) #resize the image each time to ensure consistancy
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
                self.sataliteList.remove(i) #if there's no more health left, delete the satalite
            
            self.surface.blit(i.image,i.rect) #draw satalites on screen
            
    def moveEnemies(self): #move the enemies, everyone enemy only moves once per game tick for consistancy with hit reg etc.
        for i in self.enemies: #loop through enemies
            if Enemy.changeDir == True: #If enemies are meanth to change directions
                for g in self.enemies: #loop through all enemies
                    if g.speed > 0: #Add speed to horizonal + vertical
                        g.speed += 0.4
                    else:
                        g.speed -= 0.4
                    g.y += 0.4
                    g.changeDirection() #run change direction function
                    self.surface.blit (g.image, g.rect) #draw enemies on screen
                Enemy.changeDir = False #next time tell the program not to change direction
                break #reset loop
            elif Enemy.downCount != 0 and Enemy.downCount != 1: #If the enemies are meant to be moving down
                for x in self.enemies:
                    x.moveDown() #run move down fuction
                    self.surface.blit (x.image, x.rect) #draw enemies on screen
                Enemy.downCount -= 1 #decrement down count (how manytimes enemies should be moved down)
                break #reset loop
            elif Enemy.downCount == 1: #if its the last move down
                for x in self.enemies:
                    x.moveDown() #move enemies down
                    self.surface.blit (x.image, x.rect) #draw on screen
                Enemy.changeDir = True #set next move to change direction
                Enemy.downCount -= 1 #decrement down count
                break #reset loop
            elif i.getRight() > 950 and Enemy.downCount == 0 or i.getLeft() < 50 and Enemy.downCount == 0: #if enemies hit the edge of screen
                Enemy.downCount = 50 #make them move down for 50 ticks
                break #reset loop
            i.move() #move the enemy (THIS ONLY RUNS IF LOOP IS NOT BROKEN)
            self.surface.blit (i.image, i.rect) #draw it on screen

    def shipReg(self): #Ship hit registration
        for i in self.enemies:  #if the ship collides with an enemy, kill it
            if i.rect.colliderect(self.spaceship.rect):
                self.lives = 0
                
    def enemyFire(self): #Choose a random enemy and make it shoot
        enemy = random.randint(0,len(self.enemies)-1)
        self.enemies[enemy].fire()
        
    def excecute(self): #MAIN GAMELOOP FUNCTION, WHILE TRUE RUNS EVERY TICK
        wave1 = [[1,1,1,1],[1,1,1,1]] #2d arrays for waves
        wave2 = [[1,2,1,2],[1,2,1,2]]
        wave3 = [[1,1,1,1],[2,2,2,2], [3,3,3,3]]
        
        bg = pygame.image.load("bgtemp.png") #load background
        bg = pygame.transform.scale(bg, (1000,1000)) #set screensize
        bgRect = bg.get_rect()
        bgRect.topleft = (0,0)
        self.enemies = [] #create blank enemy list
        font = pygame.font.SysFont('', 30) #set font size
        #STEVEN STUFF
        self.sataliteList = [] #create blank satalite list
        self.generateSatalite() #generate satalites 
        #//
        self.lives = 3 #default lives number
        wavecounter = 1 #wave counter
        loopcounter = 1 #loop counter
        pygame.mouse.set_visible(0) #make mouse invisible
        while True:
            if self.enemies == []: #If screen has no enemies check the wave counter and generate enemies + reinstantiate spaceship
                if wavecounter == 1:
                    self.enemies = self.generateEnemies(wave1) #generate wave 1
                    self.spaceship = Spaceship(self.surface, self.enemies, 0, (500,875), self.sataliteList) #instantiate spaceship
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
            if self.lives == 0:  #if no lives left, endgame
                self.surface.blit(font.render("Lives: "  + str(self.lives), True, (255, 255, 255)), (800, 50)) #draw lives = 0
                return self.spaceship.score #return the score to the program
                break #break game loop
            self.surface.blit(bg,bgRect) #draw enemies on scree
            self.moveEnemies() #move the enemies
            self.surface.blit(font.render("Wave: "  + str(wavecounter-1), True, (255, 255, 255)), (450, 50)) #draw wave counter
            self.surface.blit(font.render("Score: "  + str(self.spaceship.score), True, (255, 255, 255)), (100, 50)) #draw score counter
            self.surface.blit(font.render("Lives: "  + str(self.lives), True, (255, 255, 255)), (800, 50)) #draw lives counter
            #STEVEN STUFF
            self.spaceship.handle_keys() #controls keys
            self.spaceship.draw() #draws spaceship on screen
            self.drawSatalite() #draw satalites on screen
            #//
            #Bullet Handling
            self.spaceship.moveShots()#move spaceship shots
            if loopcounter == 50: #ENEMY FIRE RATE
                self.enemyFire() #every 50 gameticks, make an enemy fire
                loopcounter = 1
            for i in self.enemies: #loop through enemies
                i.moveBullets() #handle enemy firing
                if i.bullet.colliderect(self.spaceship): #enemy firing hit registration
                    i.draw = False
                    i.bullet.center = (i.rect.center[0],i.rect.bottom)
                    self.lives -= 1 #if hits spaceship reset bullet, remove a life
            #//
            self.shipReg() #handle ship hit registation
            pygame.display.update() #update display
            time.sleep (self.delay) #implement game delay (currently 0)
            loopcounter += 1 #increment counter

    
class Enemy(object):#DEFAULT ENEMY
    changeDir = False #global variables for all enemies, whether the should change direction
    downCount = 0 #how many times they should move down
    bulletSpeed = 4 #how fast their bullets move 
    def __init__(self, initPos, surface, sataliteList): 
        self.sataliteList = sataliteList #need satalite list for hit reg
        self.image = pygame.image.load("enemy1.png") #create enemy rectangle with image
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.topleft = initPos
        self.speed = 2 #USE FOR HORIZONTAL SPEED
        self.y = 2 #USE FOR VERTICAL SPEED
        self.health = 1 #USE FOR ENEMY HEALTH
        self.score = 5 #USE FOR ENEMY SCORE
        self.surface = surface #need surface to draw on
        self.bulletImg = pygame.image.load("enemybullet.png") #load bullet as rectangle
        self.bulletImg = pygame.transform.scale(self.bulletImg, (10,25))
        self.bullet = self.bulletImg.get_rect()
        self.bullet.center = (self.rect.center[0],self.rect.bottom)
        self.draw = False #variable to say whether the current enemy's bullet should be drawn on screen

    def fire(self): #fire function, draws a bullet on screen which is moved by a seperate function
        if self.draw == False: #if bullet is not already on screen, draw it
            self.bullet.center = (self.rect.center[0],self.rect.bottom)
            self.surface.blit(self.bulletImg,self.bullet)
            self.draw = True

    def moveBullets(self): #moves enemy bullets
        if self.draw == True: #if its meant to be moved
            for i in self.sataliteList: #iterate through satalites
                if i.rect.colliderect(self.bullet): #handle hit reg
                    self.draw = False #if bullet hits satalite, decrement satalite health
                    i.health -= 1
            if self.bullet.top > 1000: #if bullet hits buttom of screen, stop drawing it
                self.draw = False
            else:
                self.bullet.move_ip(0, self.bulletSpeed) #move bullet
                self.surface.blit(self.bulletImg,self.bullet) #draw bullet on screen

    def move(self): #move enemy by speed
        self.rect.move_ip(self.speed, 0)

    def changeDirection(self): #change enemy direction, move it
        self.speed = -self.speed
        self.rect.move_ip(self.speed, 0)

    def moveDown(self): #move enemy down
        self.rect.move_ip(0, self.y)

    def getRight(self): #return right of enemy
        return self.rect.right
     
    def getLeft(self): #return left of enemy
        return self.rect.left

class Enemy2(Enemy):
    def __init__(self, initPos, surface, sataliteList): #initializes enemy type 2
        self.sataliteList = sataliteList #BELOW IS SAME AS FIRST ENEMY, CAN CHANGE PROPERTIES BASED ON ENEMY TYPE
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
    def __init__(self, initPos, surface, sataliteList): #initializes enemy type 3
        self.sataliteList = sataliteList #BELOW IS SAME AS FIRST ENEMY, CAN CHANGE PROPERTIES BASED ON ENEMY TYPE
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


class Spaceship(object):
    def __init__(self, surface, enemies, score, position, sataliteList):
        # Passes in all used variables and initializes them
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
                if ev.key == pygame.K_SPACE: # fires bullet
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
                if i.colliderect(satalite): # checks for collisions between bullet and satelite
                    try:
                        self.shots.remove(i) # removes bullet
                    except:
                        pass
                    satalite.health -= 1 # Removes one from health
                    
            for x in self.enemies:
                if i.colliderect(x): # checks for collisions 
                    try:
                        self.shots.remove(i) # removes bullet
                    except:
                        pass
                    x.health -= 1 # lowers enemy health
                    if x.health == 0:
                        self.enemies.remove(x) # removes hit enemy
                    self.score += x.score # adds points to score variable
            if i.bottom < 0: # if bullet goes off screen, remove it
                self.shots.remove(i)
            else:
                i.move_ip(0, -self.bulletSpeed) # moves bullet around screen
                self.surface.blit(self.bullet,i) # blits bullet
    
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
        # Makes mouse visible
        pygame.mouse.set_visible(1)
        # creates and places asteroid
        asteroid = pygame.image.load ("asteroidIntro.png")
        asteroid = pygame.transform.scale (asteroid, (75, 75))
        asteroidRect = asteroid.get_rect (center = (75/2, 75/2))
        asteroidRect.topleft = (0, 200)
        # resets screen back to original size
        self.screen = pygame.display.set_mode (self.size)
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
            # Make asteroid reappear on other side of screen
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
        # Sets screen to white
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
                    # Runs main game loop
                    x = GameLoop()
                    score = x.excecute()
                    # Outputs game over screen
                    self.gameOver = pygame.font.SysFont ('', 90)
                    self.screen.blit (self.gameOver.render("GAME OVER", True, (255, 0, 0)), (320, 400))
                    pygame.display.update ()
                    time.sleep(4)
                    self.inputLead (score) # receives score

    def readLead (self) :
        # Reads leaderboard info from text file
        self.leaders = []
        snIn = open ("Leaderboard.txt", "r")
        while True : # Reads info from text file
            info = {}
            info ["Name"] = str.strip (snIn.readline ())
            if info ["Name"] == "" :
                break
            info ["Score"] = int(str.strip (snIn.readline ()))
            self.leaders.append (info) # appends info into list
        snIn.close () # closes file

    def outputLead (self) :
        # Outputs leaderboard info onto the screen
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
            # Outputs and orders leaderboard scores
            self.screen.blit (self.fontLead.render (str (count) + ".   ", True, (0, 255, 0)), (100, height))
            self.screen.blit (self.fontLead.render (elem ["Name"], True, (0, 255, 0)), (175, height))
            self.screen.blit (self.fontLead.render (str (elem ["Score"]), True, (0, 255, 0)), (400, height))
            pygame.display.update ()
            if count == 10 : # Iterates through 10 times to show top 10 scores
                break

        end = True
        while end :
            buttonReturn = pygame.Rect (300, 430, 200, 50) # Creates return button
            pygame.draw.rect (self.screen, [0, 255, 0], buttonReturn) 
            self.screen.blit (self.font.render('Back to Start', True, (0, 0, 0)), (325, 445)) # draws text for return button
            pygame.display.update ()

            for event in pygame.event.get ():
                if event.type == pygame.QUIT:
                    pygame.quit ()
                    sys.exit ()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if buttonReturn.collidepoint (mouse_pos) :
                        # if mouse is pressing return button, return to start screen
                        self.start ()
                        end = False

    def inputLead (self, score) :
        # Resets the screen to black
        self.bg = [0, 0, 0]
        self.screen.fill (self.bg)

        # Inputs the info for the current user and adds it to a text file
        snOut = open ("Leaderboard.txt", "a")
        name = ""
        font = pygame.font.Font (None, 50)
        end = True
        while end :
            for evt in pygame.event.get() : # Checks for events
                if evt.type == KEYDOWN : # If the event is a keypress
                    if evt.unicode.isalpha () : # Finds the unicode value for keypress
                        name += evt.unicode # adds value to name
                    elif evt.key == K_BACKSPACE : # Removes last character from name
                        name = name[:-1]
                    elif evt.key == K_RETURN :
                        # Ends loop and adds info to text file
                        end = False
                        if len(name) > 10: # Long name handling
                            name = name[ :9]
                        # outputs info into text file
                        snOut.write (name + "\n")
                        snOut.write (str (score) + "\n")
                        snOut.close ()
                        # Restarts opening screen
                        self.start ()
            # Outputs current inputted name
            self.screen.fill (self.bg)
            self.screen.blit (self.fontTitle.render('Please enter your name:', True, (0, 255, 0)), (100, 100))
            # Renders location for name to be outputted
            block = font.render(name, True, (0, 255, 0))
            rect = block.get_rect()
            # Places in center of screen
            rect.center = self.screen.get_rect().center
            self.screen.blit(block, rect)
            pygame.display.flip()
# Starts program
x = Menu ()
x.start ()
