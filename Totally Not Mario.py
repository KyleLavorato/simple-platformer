#mainclass

import pygame, os, time

from pygame.locals import *
from tkinter import*
import math
import random
pygame.init()

##WINDOW_WIDTH = 45*29
##WINDOW_HEIGHT = 25*29
##surface = pygame.display.set_mode ((WINDOW_WIDTH, WINDOW_HEIGHT),0,32)

class Mainclass:
    def __init__(self):
        pygame.init()
        self.WINDOW_WIDTH = 45*29
        self.WINDOW_HEIGHT = 25*29
        self.screen = pygame.display.set_mode ((self.WINDOW_WIDTH, self.WINDOW_HEIGHT),0,32)
        self.score = 0 # The player's score
        self.deaths=0 # The player's deaths
        self.level = 0
        self.levelSelect = True
        self.buttonList = []
        self.run = True
        self.instRun=True # Runs the instructions function
        self.clock = pygame.time.Clock()
        self.onScreen = pygame.sprite.Group()
        self.userEvents = {'SCREEN_EXIT':USEREVENT+1, 'PLAYER_KILL':USEREVENT+2, 'COIN_COLLECT':USEREVENT+3, 'BOUNCE_GOO':USEREVENT+4, 'LEVEL_DONE':USEREVENT+5 , 'JihadNoise':USEREVENT+6}
        self.player = Player (self.screen, self.onScreen, self.userEvents)
        self.font=pygame.font.SysFont("Arial",24) # Defines a font to be used to create text objects
        self.scoreText=self.font.render("Score: "+str(self.score),1,(255,255,255)) # The score counter
        self.deathText=self.font.render("Deaths: "+str(self.deaths),1,(255,255,255)) # The death counter
        self.instText=self.font.render("Instructions",1,(255,255,255)) # Title for instructions screen
        self.contText=self.font.render("Controls",1,(255,255,255)) # Title for instructions screen
        self.message = self.font.render("The Adventure Has Just Begun",1,(0,0,0))
        self.instruct=[] # Empty list to hold all the rendered block description text
        self.controlText=[] # Empty list to hold all the rendered control text
        self.backgroundPic=pygame.image.load("Graphics/background.jpg") # Loads the background image for the main screen
        self.backgroundPic=pygame.transform.scale(self.backgroundPic, (45*29, 25*29)) # Scales the image to fit in the pygame window
        self.levelSelectPic = pygame.image.load("Graphics/LevelSelect.jpg")
        self.levelSelectPic=pygame.transform.scale(self.levelSelectPic, (45*29, 25*29)) # Scales the image to fit in the pygame window   
        #self.finalPic = pygame.image.load("Graphics/Map.jpg")  #This is the final screen
        self.finalPic = pygame.image.load("Graphics/FinalScreen.jpg")
        self.finalPic = pygame.transform.scale(self.finalPic, (45*29, 25*29))
        self.wallPic=pygame.image.load("Graphics/wallb.jpg") # Loads the background image for the instructions screen
        self.wallPic=pygame.transform.scale(self.wallPic, (45*29, 25*29)) # Scales the image to fit in the pygame window
        self.controlList=["Move left","Move right","Jump","Respawn when dead"] # List of all the controls to render text objects
        self.textList=["Kills you","Kills you","Level finish","Spring jump","Spawn block","Disapperaing Block","Increases Score"] # List of all the player interactive block descriptions to render text objects
        self.imageList=[pygame.image.load('Graphics/spike2.png'), pygame.image.load('Graphics/red_square.png'), pygame.image.load('Graphics/door.png'), pygame.image.load('Graphics/blu.png'), pygame.image.load('Graphics/orange.png'), pygame.image.load('Graphics/disap.png'), pygame.image.load('Graphics/coin_0.png')] # List of all the player interactive block images
        self.controlImage=[pygame.image.load('Graphics/a_key.png'), pygame.image.load('Graphics/left_arrow.png'), pygame.image.load('Graphics/d_key.png'), pygame.image.load('Graphics/right_arrow.png'), pygame.image.load('Graphics/w_key.png'), pygame.image.load('Graphics/up_arrow.png'), pygame.image.load('Graphics/spacebar.png')] # List of all the control images
        for i in range(0,len(self.controlImage)-1):
            self.controlImage[i]=pygame.transform.scale(self.controlImage[i], (32, 32)) # Scales all the square images for controls to proper
        self.controlImage[len(self.controlImage)-1]=pygame.transform.scale(self.controlImage[len(self.controlImage)-1], (200, 32)) # Scales the spacebar image seperatly to keep proper rectangular aspect ratio
        for i in range(0,len(self.textList)):
            self.temp=self.font.render(self.textList[i],1,(255,255,255)) # Renders all the block descriptions into placable text objects and adds them to the releveant list
            self.instruct.append(self.temp)
        for i in range(0,len(self.controlList)):
            self.temp=self.font.render(self.controlList[i],1,(255,255,255)) # Renders all the controls text into placable text objects and adds them to the releveant list
            self.controlText.append(self.temp)
        pygame.mixer.init(22050, -16, 2, 256) #Initializes the pygame sound mixer with default values except for a lowered buffer to reduce latency
        self.menuTunes=pygame.mixer.Sound("Sounds/grimrock.wav") # Loads the main menu music
        #self.menuTunes=pygame.mixer.Sound("Sounds/still_alive.wav") # Loads the menu music
        self.endTunes=pygame.mixer.Sound("Sounds/Wiggle.wav")
        self.easterEgg = pygame.mixer.Sound("Sounds/Jihad.wav")
        self.coinDing=pygame.mixer.Sound("Sounds/coin.wav") # Loads the sound for getting coins
        self.musicList=[pygame.mixer.Sound("Sounds/LevelMusic/game_music.wav"),pygame.mixer.Sound("Sounds/LevelMusic/skyrim_8_bit.wav"),pygame.mixer.Sound("Sounds/LevelMusic/still_alive.wav"),pygame.mixer.Sound("Sounds/LevelMusic/8_bit_adventure.wav"),pygame.mixer.Sound("Sounds/LevelMusic/blackout_city.wav"), pygame.mixer.Sound("Sounds/LevelMusic/rick_roll.wav"), pygame.mixer.Sound("Sounds/LevelMusic/chip.wav"), pygame.mixer.Sound("Sounds/LevelMusic/pewpew.wav"),pygame.mixer.Sound("Sounds/LevelMusic/red_flag.wav"),pygame.mixer.Sound("Sounds/LevelMusic/Castlevania.wav")] # Loads a list of all the music tracks for the levels
        self.originalMList=[x for x in self.musicList] # Creates a copy to restore the list at loop time
        self.trackNumber=0 # Counter variable for the current level track being played
        self.coinFrames=[pygame.image.load('Graphics/coin_0.png'),pygame.image.load('Graphics/coin_1.png'),pygame.image.load('Graphics/coin_2.png'),pygame.image.load('Graphics/coin_3.png')] # Loads the coin .gif frame by frame
        self.boxImages=[pygame.image.load('Graphics/spike2.png'),pygame.image.load('Graphics/red_square.png'),pygame.image.load('Graphics/wall.png'),pygame.image.load('Graphics/door.png'),pygame.image.load('Graphics/blu.png'),pygame.image.load('Graphics/orange.png'),pygame.image.load('Graphics/disap.png')] # Loads all the block graphics needed by the box classes
        self.boxImages.append(self.coinFrames) # Appends the list of coin frames to the graphics list
        self.levelList = []
        self.loadLevels()
        self.invincible = False
        self.jihadMode=False # Value for if jihad mode is active or not
        self.deathNoise=pygame.mixer.Sound('Sounds/explosion.wav') # Loads the death noise for jihad mode
        self.jihadText=[] # Empty list to hold all the jihad mode text objects
        self.jihadFont=pygame.font.SysFont('Impact',42) # Creates a new font
        self.jihadCount=0 # Counter variable for the jihad text
        # Creates 100 rendered text objects with different colours and adds them to the list
        for i in range(0,100):
            self.temp=self.jihadFont.render("JIHAD MODE",1,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            self.jihadText.append(self.temp)
        #print(self.jihadText[0].get_width())
        self.menu()

    def instructions(self):
        self.screen.blit(self.wallPic,(0,0)) # Blits the instructions menu background image to the screen
        self.backButton = []
        # Block Instructions
        self.x=self.WINDOW_WIDTH//2 # Sets the x value for the items to half the window width
        self.x+=self.WINDOW_WIDTH//4 # Sets the x value to be in the right side of the screen
        self.y=self.WINDOW_HEIGHT//10 # Sets the y value to be evenly spaced by dividing the height into 10
        self.screen.blit(self.instText,(self.x-(self.WINDOW_WIDTH//2//2//2//2),self.y)) # Blits the "Instructions" title to the screen
        self.y+=self.WINDOW_HEIGHT//10 # Increases the y value for the next item
        for i in range(0,len(self.instruct)):
            self.screen.blit(self.instruct[i],(self.x,self.y)) # Blits the text description to the screen
            self.screen.blit(self.imageList[i],(self.x-100,self.y)) # Blits the block graphic to the screen to the left of the text
            self.y+=self.WINDOW_HEIGHT//10 # Increases the y value for the next item

        # Controls
        self.counter=0 # Sets a counter variable to zero
        self.x=self.WINDOW_WIDTH//2 # Sets the x value for the items to half the window width
        self.x+=-self.WINDOW_WIDTH//4 # Sets the x value to be in the left side of the screen
        self.y=self.WINDOW_HEIGHT//10 # Sets the y value to be evenly spaced by dividing the height into 10
        self.screen.blit(self.contText,(self.x-(self.WINDOW_WIDTH//2//2//2//2),self.y)) # Blits the "Controls" title to the screen
        self.y+=self.WINDOW_HEIGHT//10 # Increases the y value for the next item
        for i in range(0,len(self.controlText)):
            self.screen.blit(self.controlText[i],(self.x,self.y)) # Blit the control text to the screen
            if self.counter>4:
                self.screen.blit(self.controlImage[self.counter],(self.x-265,self.y)) # If at the last element of the list, blit the picture further to the left as the spacebar graphic is much wider
            else:
                self.screen.blit(self.controlImage[self.counter],(self.x-100,self.y)) # Blit the first key image to the screen
            try:
                self.screen.blit(self.controlImage[self.counter+1],(self.x-142,self.y)) # Blit the second control key for that action to the screen if acceptable as the last control (space) does not have a matching key for teh same control
            except:
                pass
            self.counter+=2 # Increases the counter to select the proper elements of the list nex time through the loop
            self.y+=self.WINDOW_HEIGHT//10 # Increases the y value for the next item
        
        self.backButton.append (createButton(self.screen,(560,650,170,40),"Back"))
            
        while self.instRun:
            for e in pygame.event.get():
                self.backButton[0].event (e)
            if self.backButton[0].play == True:
                self.instRun = False
            pygame.display.update()
        self.screen.blit(self.backgroundPic,(0,0)) # Blits the main menu background image back to the screen for the transition to the screen
    def levelSelectScreen(self): 
        self.screen.blit (self.levelSelectPic,(0,0))
        self.EnterButton = createButton(self.screen,(560,300,170,40),"Enter")#creates the enter button
        self.menuButton = createButton(self.screen,(560,500,170,40),"Main Menu") #creates the button to go back to the main menu
        self.levelSelection = '' #the number that will be entered to select the level
        self.enterName() #calls enter name to display the written text
        while self.levelSelect:
            for e in pygame.event.get():
                self.EnterButton.event(e)
                self.menuButton.event(e)
                if e.type == KEYDOWN: #If the user presses any key 
                    if len(self.levelSelection) < 2: #If the length of the name the user has entered is less than 8 
                        if 122 >= e.key >= 97 or 90 >= e.key >= 65 or 57 >= e.key >= 48 or e.key == 32: #Check if the key pressed is a letter, number, or space 
                            if e.mod and KMOD_SHIFT: #If the user is pressing shift, or caps lock 
                                self.levelSelection+=str.upper(chr(e.key)) #Add a cappital version of the key pressed to the name
                            else: #Else, if the user is not using caps 
                                self.levelSelection+=chr(e.key) #Add the lowercase version of the character to the name
                    if e.key == K_BACKSPACE: #If the user pressed backspace 
                        self.levelSelection = self.levelSelection[:-1] #Remove the last letter in the name
            if self.EnterButton.play == True:
                if 0 < int(self.levelSelection) <= len(self.levelList): #Ensures level selection is valid
                    self.level = int(self.levelSelection)-1 #subtracts one from the level so that it uses the approiate list number
                else:
                    self.level = 0
                self.start() #starts
                self.buttonList[2].play = False#makes sure the levelSelect screen does not come back immediately
            if self.menuButton.play == True:
                self.levelSelect = False
            self.EnterButton.draw() #redraws the two buttons so they don't disappear
            self.menuButton.draw()
            self.enterName() #updates what the user has written
            pygame.display.update()
            self.screen.blit(self.levelSelectPic,(0,0))

    def menu (self):
        self.menuTunes.play(loops=-1) # Starts playing the menu music on an endless loop
        self.screen.blit(self.backgroundPic,(0,0)) # Blits the main menu background image to the screen
        self.buttonList.append(createButton(self.screen,(550,100,170,40),"Play Game"))
        self.buttonList.append(createButton(self.screen,(550,200,170,40),"Instructions"))
        self.buttonList.append(createButton(self.screen,(550,300,170,40),"Level Select"))
        self.buttonList.append(createButton (self.screen,(550,400,170,40),"Level Creator"))
        
        while True:
            for e in pygame.event.get():
                #checks to see if any button has been pressed
                self.buttonList[0].event(e)
                self.buttonList[1].event(e)
                self.buttonList[2].event(e)
                self.buttonList[3].event(e)
                if e.type == QUIT:
                    self.menuTunes.stop()
                    pygame.quit()
                    os._exit(1)
            if self.buttonList[0].play == True:
                self.start () #starts the game
                #break
            if self.buttonList[1].play == True:
                self.instructions() #goes to the instructions screen
                self.buttonList[1].play = False
                self.instRun = True
            if self.buttonList[2].play == True:
                self.levelSelectScreen() #goes to the level select screen
                self.buttonList[2].play = False
                self.levelSelect = True
            if self.buttonList[3].play == True:
                self.levelCreate = LevelCreator() #goes the the level creator
                self.buttonList[3].play = False
            for i in range (len(self.buttonList)):
                self.buttonList[i].draw() #redraws the buttons so they will not disappear
            pygame.display.update()
            self.screen.blit(self.backgroundPic,(0,0))
        
    def loadLevels (self):
        i = 0
        while True:
            i +=1
            try:
                #loads the levels into a list
                #The levels are all stored the same with the exception of the level number on the end
                #the i adds the number getting all the level files and exiting when there are no more
                #levels to be added to the list
                self.levelList.append (Level('levels/level'+str(i), self.screen, self.onScreen, self.userEvents,self.boxImages))
            except:
                break
        
    def start (self):
        self.menuTunes.fadeout(150) # Causes the music to fade out for 2secs
        self.currentLevel = self.levelList[self.level]
        self.trackNumber=random.randint(0,len(self.musicList)-1)
        self.musicList[self.trackNumber].play(loops=-1) # Plays the current track for the level background music
        self.currentLevel.currentGrid.load()
        self.player.spawn()
        
        self.multiplier = 1
        while self.run:
            self.addDeaths = 0
            self.tick = self.clock.tick (60)
            for event in pygame.event.get():
                if event.type == self.userEvents["SCREEN_EXIT"]: #When they exit the screen it finds the next grid to be placed
                    self.currentLevel.nextGrid(event.side)
                    for block in self.onScreen.sprites():
                        if block.type == 4:
                            block.replace()
                if event.type == QUIT:
                    self.run = False
                if event.type == self.userEvents["COIN_COLLECT"]:
                    self.score+=100*self.multiplier #adds 100 x the multiplier to the score when a coin is collected
                    self.score = round(self.score)
                    self.multiplier += .2 #increases the multiplier when a coin is hit
                    if self.multiplier >= 2:
                        self.multiplier = 2
                    self.coinDing.play()
                if event.type == self.userEvents["BOUNCE_GOO"]:
                    self.player.yVel=-1.8 #bounces the player up extra height
                if event.type == self.userEvents["LEVEL_DONE"]:
                    self.musicList[self.trackNumber].fadeout(150) # Ends the current music track
                    del self.musicList[self.trackNumber]
                    self.level+=1 #adds one to the level number
                    try:self.currentLevel = self.levelList[self.level] #tries to get the next level folder
                    except IndexError:
                        self.end () #if there is no more level folders it will go to the end screen
                    else:
                        self.currentLevel.currentGrid.load()
                        self.player.spawn()
                        #print(self.musicList)
                        #print(self.trackNumber)
                        if len(self.musicList)==0:
                            self.musicList=[x for x in self.originalMList] # Restores the tracklist to default for looping
                        if len(self.musicList)==1:
                            self.trackNumber=0
                        else:
                            self.trackNumber=random.randint(0,len(self.musicList)-1) # Picks a new song in the list
                        self.musicList[self.trackNumber].play(loops=-1) # Begins the music for the next level
                if event.type == KEYDOWN:
                    if event.key == K_i:
                        self.invincible = not self.invincible
                if event.type == self.userEvents["PLAYER_KILL"]:
                    if not self.invincible:
                        self.addDeaths += 1 #adds one to the death count
                        self.multiplier = 1 #resets the multiplier when you die
                        if self.jihadMode==True:
                            self.deathNoise.play() # Plays the death noise when jihad mode is active
                        self.player.kill(self.jihadMode) #does death animation
                        for block in self.onScreen.sprites():
                            if block.type == 4:
                                block.replace()
                if event.type == self.userEvents["JihadNoise"]:
                    if self.jihadMode==False:
                        self.easterEgg.play(loops=-1) # Activetes the jihad mode soundtrack
                        self.jihadMode=True # Sets jihad mode to active
                        self.score+=50000 # Gives the player a score bonus
                    else:
                        pass
            if self.addDeaths >1:
                self.addDeaths = 1 #if the death count is being added by two due to the collision with two death blocks, it will bring it down to one
            self.deaths += self.addDeaths #adds to the total death count
                    
            self.onScreen.update()
            self.player.update ()
            self.screen.blit(self.scoreText,(0,0)) #puts the score on the screen
            self.screen.blit(self.deathText,((self.screen.get_width()-self.deathText.get_width()),0)) #puts the number of deaths on the screen
            if self.jihadMode==True:
                self.screen.blit(self.jihadText[self.jihadCount],(self.WINDOW_WIDTH//2-(self.jihadText[self.jihadCount].get_width()//2),self.WINDOW_HEIGHT//12)) # Blit the jihad mode text to the screen
                self.jihadCount+=1 # Increases the counter variable
                if self.jihadCount==len(self.jihadText):
                    self.jihadCount=0 # Resets the counter to use again
            pygame.display.update()
            self.screen.fill ((150,200,255))
            self.scoreText=self.font.render("Score: "+str(self.score),1,(255,255,255))#updates the score text
            self.deathText=self.font.render("Deaths: "+str(self.deaths),1,(255,255,255)) #updates the death text

        pygame.quit ()
    #def finish (self):
    def end (self):
        self.endTunes.play(loops=-1) #starts the final song
        self.scoreText=self.font.render("Final Score: "+str(self.score),1,(0,0,0)) #updates the score to final score
        self.deathText=self.font.render("Final Deaths: "+str(self.deaths),1,(0,0,0)) #updates the deaths to final deaths
        self.screen.blit (self.finalPic,(0,0)) #puts the final background
        self.screen.blit(self.scoreText, (0,0)) #puts the final score
        self.screen.blit(self.deathText,((self.screen.get_width()-self.deathText.get_width()),0)) #puts the final deaths
        self.screen.blit(self.message,((self.WINDOW_WIDTH//2//2*1.5),25*27)) # This will be the message at the end.
        pygame.display.update()
        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.menuTunes.stop()
                    pygame.quit()
                    os._exit(1)
        self.run = False
    def enterName(self): #Function which displays a menu allowing the user to enter their name    
        self.enterNameLabel = self.font.render("Enter the level you want to start at:", 1, (255, 255, 255)) #Creates and renders the text "Enter your name:" in the center of the screen 
        self.screen.blit(self.enterNameLabel, (500, 260))

        nameLabel = self.font.render(self.levelSelection, 1, (255, 255, 255)) #renders what the user has typed so far to the screen within the textbox 
        self.screen.blit(nameLabel, (800, 260))
      

class Level:
    '''Creates an object for each level of the game'''
    def __init__(self,folderName,screen,group, userEvents, boxImages):
        '''Constructs the class'''
        self.boxImages=boxImages
        self.screen=screen
        self.onScreen=group
        self.folderName=folderName
        self.gridNumber=0
        self.userEvents = userEvents
        self.grids=[]
        self.openFiles()
        self.currentGrid=self.grids[0]
        #self.currentGrid.load()   
    def openFiles(self):
        '''Opens the individual grid files and creates Grid objects to store in a list'''
        while True:
            try:
                self.gridNumber+=1
                self.snIn=open(self.folderName+'/grid'+str(self.gridNumber)+".txt",'r')
                self.grids.append(Grid(self.snIn,self.screen,self.onScreen, self.userEvents,self.boxImages))
            except:
                break
    def nextGrid (self,side):
        '''Moves to the next grid in the list'''
        self.currentGrid = self.grids[self.currentGrid.getNext(side)-1]
        self.currentGrid.load()

class Grid:
    '''Creates an object for each grid (section) of the level'''
    def __init__(self,streamNumber,screen,group, userEvents,boxImages):
        '''Constructs the class'''
        self.boxImages=boxImages
        self.snIn=streamNumber
        self.screen=screen
        self.onScreen=group
        self.userEvents = userEvents
        self.loadGrid()
    def getNext(self, side):
        '''Returns the next grid number'''
        return int(self.directions[side])
    def loadGrid(self):
        '''Loads a 2D list of Block sprites from a txt file'''
        self.directions=str.strip(self.snIn.readline())
        self.directions=self.directions.split(',')
        self.grid=[]
        for i in range(0,25):
            self.row=str.strip(self.snIn.readline())
            self.row=self.row.split(',')
            for i, box in enumerate(self.row):
                self.row[i] = box.split(';')
            self.grid.append(self.row)
        for i in range(0,25):
            for j in range(0,45):
                if self.grid[i][j][0]=='1':
                    self.grid[i][j]=Platform(self.screen,j*29,i*29, self.userEvents,self.boxImages)
                elif self.grid[i][j][0]=='2':
                    self.grid[i][j]=Spyke(self.screen,j*29,i*29, self.userEvents, int(self.grid[i][j][1]),self.boxImages)
                elif self.grid[i][j][0]=='3':
                    self.grid[i][j]=BlueGoo(self.screen,j*29,i*29, self.userEvents,self.boxImages)
                elif self.grid[i][j][0]=='4':
                    self.grid[i][j]=Disappear(self.screen,j*29,i*29, self.userEvents,self.boxImages)
                elif self.grid[i][j][0]=='5':
                    self.grid[i][j]=Death(self.screen,j*29,i*29, self.userEvents,self.boxImages)
                elif self.grid[i][j][0]=='6':
                    self.grid[i][j]=Coin(self.screen,j*29,i*29, self.userEvents,self.boxImages)
                elif self.grid[i][j][0]=='7':
                    self.grid[i][j]=Goal(self.screen,j*29,i*29, self.userEvents,self.boxImages)
                elif self.grid[i][j][0]=='8':
                    self.grid[i][j]=Spawn(self.screen,j*29,i*29, self.userEvents,self.boxImages)
                elif self.grid[i][j][0]=='9':
                    self.grid[i][j]=Jihad(self.screen,j*29,i*29, self.userEvents,self.boxImages)
                else:
                    self.grid[i][j]=0
    def load(self):
        '''Loads a 2D list of Block sprites onto the screen'''
        self.onScreen.empty()
        for row in self.grid:
            for box in row:
                if box:
                    self.onScreen.add(box)

class Player(pygame.sprite.Sprite): #Player class: handles movement, collision detection, and other player related functions
    def __init__(self, screen, blocks, userEvents):
        '''Initializes Variables'''
        pygame.sprite.Sprite.__init__(self) #Inherits from Sprite class; call sprite initialization
        self.background=pygame.image.load('Graphics/jihad_death.jpg').convert() # Loads jihad death screen image
        self.background=pygame.transform.scale(self.background, (45*29, 25*29)) # Resizes jihad death screen image
        self.background.set_alpha(200) # Sets jihad death screen image opacity to 200/255
        #Loads player (mario) sprite images
        self.images = {'still':pygame.transform.scale(pygame.image.load('Graphics/mario-still.png'), (29, 54)), 'right':pygame.transform.scale(pygame.image.load('Graphics/mario-right.png'), (29, 54)), 'left':pygame.transform.scale(pygame.image.load('Graphics/mario-left.png'), (29, 54)), 'jump-right':pygame.transform.scale(pygame.image.load('Graphics/mario-jump-right.png'), (29, 54)), 'jump-left':pygame.transform.scale(pygame.image.load('Graphics/mario-jump-left.png'), (29, 54))}
        self.image = self.images['still'] #Sets current image
        self.rect = self.image.get_rect() #Gets rect from current image
        self.screen = screen #Screen surface
        self.blocks = blocks #List of blocks (on Screen)
        self.userEvents = userEvents #Dict of user defined events
        self.xVel, self.yVel = 0, 0 #Vertical and horizontal velocities
        self.onGround = False #player on ground or not
        self.onWall = False #Player touching wall or not
        self.dead = False #Is player dead
        self.alive = False #Is player alive
        self.clock = pygame.time.Clock() #Clock
        self.spawn() #Spawn player
        self.update() #Update player
                    
    def update(self):
        '''Updates player location'''
        if self.dead: #Blits death message to screen if player dead
            self.screen.blit(self.deathMessage, (0, 0, self.screen.get_width(), self.screen.get_height()))
            if pygame.key.get_pressed()[K_SPACE]:
                self.spawn() #Respawn if user presses space
            else:
                return #Else returns to exit function (such that the player is not drawn to the screen)
        if not self.alive: #If player is not alive exit function
            return
        
        self.timedelta = self.clock.tick() #Time between last time this function was called
        if self.timedelta > 100: #Ensures timedelta does not fall above 100 such that the player does not glitch through walls and stuff
            self.timedelta = 50
            
        keys = pygame.key.get_pressed() #Gets a list of keys that are being pressed
        if keys[K_LEFT] or keys[K_a]: #If the left arrow key or A key are pressed
            self.xVel = max(-3, self.xVel - self.timedelta / 50) #Decrease the velocity on the x axis to a minimum of -3
        elif keys[K_RIGHT] or keys[K_d]: #If the right arrow key or D key are pressed
            self.xVel = min(3, self.xVel + self.timedelta / 50) #Increase the velocity on the x axis to a maximum of 3
        else: #Else if neither right or left are being pressed
            self.xVel = math.copysign(max(abs(self.xVel)-self.timedelta / 100, 0), self.xVel) #Reduce the x velocity aproaching zero
        if keys[K_UP] or keys[K_w]: #If the up arrow key or W key are pressed
            if self.onGround: #If player is on the ground
                self.yVel = -1.3 #Set vertical velocity to -1.3 (jump)
                self.onGround = False 
            if self.onWall == 'right': #If player is on a wall to the right
                self.yVel = -1.3 #Set y and x velocity such that the player jumps to the left
                self.xVel += -3 
            if self.onWall == 'left': #If player is on a wall to the left
                self.yVel = -1.3#Set y and x velocity such that the player jumps to the right
                self.xVel += 3
                
                
        self.yVel = min(1, self.yVel + 2 * self.timedelta / 400) #Increase vertical velocity (Simulates gravity)
        if not self.onGround: #If the player is not on the ground and touching a wall
            if self.onWall:
                self.yVel = min(0.5, self.yVel + 2 * self.timedelta / 300) #Increases vertical velocity (at a slower rate)
        
        self.rect = self.rect.move(self.xVel * self.timedelta / 4,0) #Moves player along the x axis 
        self.onWall = False #Sets on wall to false
        self.detectCollisions(self.xVel, 0) #Checks for collisions (along the x axis)
        
        self.rect = self.rect.move(0, self.yVel * self.timedelta) #Moves player along the y axis
        self.onGround = False #Sets on ground to false
        self.detectCollisions(0, self.yVel) #Checks for collisions (along the y axis)
        
        if self.xVel > 0: #If moving right
            if self.onGround: #And on ground
                self.image = self.images['right'] #Use running right image
            else: #And not on ground
                self.image = self.images['jump-right'] #Use rumping to the right image
        elif self.xVel < 0: #If moving left
            if self.onGround:  #And on ground
                self.image = self.images['left'] #Use running left image
            else: #And not on ground
                self.image = self.images['jump-left'] #Use jumping left image
        else: #If not moving left or right
            if self.onGround: #And on ground
                self.image = self.images['still'] #Use standing still image
            else: #And not on ground
                self.image = self.images['jump-right'] #Use jumping right image (Dont have a jumping normally image so this will have to do)
        self.checkExit() #Checks if the player exited the screen
        self.screen.blit(self.image, self.rect) #Blits player to the screen

    def detectCollisions(self, xVel, yVel):
        '''Handles collision detection between the player and the list of blocks'''
        for block in pygame.sprite.spritecollide(self, self.blocks, False): #Loops through the block sprites that collide with the player 
            if block.collide: #If the block is collidable
                if xVel > 0: #If moving right
                    block.collision('left') #Block was collided with on left side
                    if block.type != 6: #If block is not a coin
                        self.onWall = 'right' #Player is on wall on his right
                        self.rect.right = block.rect.left #Move right side of player to the left side of the block
                        self.xVel =0 #Stop horizontal movement
                if xVel < 0: #If moving left
                    block.collision('right') #Block was collided with on right side
                    if block.type != 6: #If block is not a coin
                        self.onWall = 'left' #Player is on wall on his left
                        self.rect.left = block.rect.right #Move right side of player to the left side of the block
                        self.xVel=0 #Stop horizontal movement
                if yVel > 0: #If moving down
                    block.collision('top') #Block was collided with on the top
                    if block.type != 6: #If block was not a coin
                        self.rect.bottom = block.rect.top #Set bottom of player to top of block
                        self.onGround = True #Player is on the ground
                        self.yVel = 0 #Stop vertical movement
                if yVel < 0: #If moving up
                    block.collision('bottom') #Block was collided with on the bottom
                    if block.type != 6: #If block was not a coin
                        self.rect.top = block.rect.bottom #Move top of player to bottom of block
                        self.yVel = 0 #Stop vertical movement

    def checkExit(self):
        '''Checks if player exited sides of screen'''
        if self.rect.center[0] < 0: #If center of player past left side of screen
            pygame.event.post(pygame.event.Event(self.userEvents['SCREEN_EXIT'], side = 2)) #Post Screen exit event with side property of 2
            self.rect.x += self.screen.get_width() #Move player to right side of screen
        if self.rect.center[0] > self.screen.get_width():#If center of player past right side of screen
            pygame.event.post(pygame.event.Event(self.userEvents['SCREEN_EXIT'], side = 0)) #Post screen exit event with side property of 0
            self.rect.x -= self.screen.get_width() #Move player to left side of screen
        if self.rect.center[1] < 0: #If player center past top of screen
            pygame.event.post(pygame.event.Event(self.userEvents['SCREEN_EXIT'], side = 3)) #Post screen exit event with side property of 3
            self.rect.y += self.screen.get_height() #Move player to bottom of screen
        if self.rect.center[1] > self.screen.get_height(): #If center of player past bottom of screen
            pygame.event.post(pygame.event.Event(self.userEvents['SCREEN_EXIT'], side = 1)) #Post screen exit event with side property of 1
            self.rect.y -= self.screen.get_height() #Move player to top of screen

    def kill(self,jihadMode):
        '''Kills the player'''
        pygame.sprite.Sprite.kill(self) #Inherits from the sprite kill method
        self.xVel = 0 #Reset vertical and horizontal velocity
        self.yVel = 0
        self.deathMessage = pygame.Surface((self.screen.get_width(), self.screen.get_height()), flags = SRCALPHA) #Creates death screen surface (with transparency enabled)
        self.deathFont = pygame.font.SysFont('Impact', 64) #Creates font for use in the deathscreen
        if jihadMode==True: #If jihad mode enabled; kyle y u do dis 
            self.deathMessage.blit(self.background,(0,0))
            self.deathText = self.deathFont.render('Jihad Failed', True, (255, 255, 255))
            self.deathTextRect = self.deathText.get_rect()
            self.deathTextRect.center = self.deathMessage.get_rect().center
            self.deathTextRect.top-=100
            self.deathMessage.blit(self.deathText, self.deathTextRect)
            self.respawnFont = pygame.font.SysFont('Arial', 32)
            self.respawnText = self.respawnFont.render('Press space to jihad again.', True, (255, 255, 255))
        else:
            self.deathMessage.fill((255, 0, 0, 200)) #Fill death screen with red and an transparency value of 200
            self.deathText = self.deathFont.render('YOU SUPA DEAD YO', True, (255, 255, 255)) #Creates death text
            self.deathTextRect = self.deathText.get_rect() #Gets rect from death text
            self.deathTextRect.center = self.deathMessage.get_rect().center #Moves death text to center of screen
            self.deathMessage.blit(self.deathText, self.deathTextRect) #Blits death text to screen
            self.respawnFont = pygame.font.SysFont('Arial', 32) #Creates font for respawn message
            self.respawnText = self.respawnFont.render('Press space to respawn.', True, (255, 255, 255)) #Creates respawn message
        self.respawnTextRect = self.respawnText.get_rect() #gets rect from respawn message
        self.respawnTextRect.midtop = self.deathTextRect.midbottom #centers the respawn message
        self.respawnTextRect.top -= 7 #Raises it slightly
        self.deathMessage.blit(self.respawnText, self.respawnTextRect) #Blits respawn message to death message surface
        self.screen.blit(self.deathMessage, (0, 0, self.screen.get_width(), self.screen.get_height())) #Blits death message surface to screen
        self.dead = True #Player is dead
        self.alive = False #Player is not alive

    def spawn(self):
        '''Spawns the player'''
        for block in self.blocks.sprites(): #loop through list of blocks
            if block.type == 8: #If block is a spawn block
                self.dead=False #Player is not dead
                self.alive=True #Player is alive
                self.rect.midbottom = block.rect.midbottom #Moves player location to location of spawn block


class createButton: #Class used to create and modify buttons
    def __init__(self,surface, rect, text="<Button Text Here>",  callback="", bgColor=(200, 200, 200), textColor=(0, 0, 0), fontSize=24): #Initialization function which creates and saves variables for various button properties as soon as a button is created with the class
        # All properties of the button are passed into the class as parameters, and saved in the variable self.
        # self references the variable that was assigned to this class, this way we can easily store variables seperatly for each button without creating global lists  
        self.WINDOW_WIDTH = 45*29
        self.WINDOW_HEIGHT = 25*29
        self.surface = surface
        self.play = False
        self.rect = rect #variable containing the dimensions for the button
        self.xPos, self.yPos, self.width, self.height = self.rect #Gets the x position, y position, width and height from the rect variable, and gives them their own variables
        self.text = text #Variable containing the text to be displayed on the button
        self.callback = callback #Variable containing the command to be executed when the button is clicked
        self.bgColor = bgColor #Variable containing the background color for the button
        self.textColor = textColor #Variable containing the text color for the button
        self.fontSize = fontSize #Variable containing the font size
        self.font = pygame.font.SysFont("Verdana", self.fontSize) #Creates a font with the specified font size
        self.state="UP" #Variable containing the state of the button, defaults to UP
        self.hover=False #Variable containing whether or not the mouse is hovering over top of the button

    def draw(self): #Method which draws the button
        if self.hover: #If the mouse is hovering over the button
            rgb = [x + 20 for x in self.bgColor] #Get the buttons background color, and increases each rgb value by 20 (lightening the color)
            if rgb[0]>255: #if the value is greater than 255
                rgb[0]=255 #set it to 255
            if rgb[1]>255: #if the value is greater than 255
                rgb[1]=255 #set it to 255
            if rgb[2]>255: #if the value is greater than 255
                rgb[2]=255 #set it to 255
            self.button = pygame.draw.rect(self.surface, rgb, self.rect) #Draws the background for the button with a slightly lighter color
        else: #Else, if the mouse is not hovering over the button
            self.button = pygame.draw.rect(self.surface, self.bgColor, self.rect) #Draw the buttons background with the normal background color
            
        if self.state == "UP":  #If the state of the mouse is up
                                #Draws the mouse button, with highlights and shadows to appear extruded
            pygame.draw.rect(self.surface, (0, 0, 0), self.rect, 1)#Black boarder
            pygame.draw.line(self.surface, (255, 255, 255), (self.xPos+1, self.yPos+1), (self.xPos+self.width-2, self.yPos+1)) #White highlights
            pygame.draw.line(self.surface, (255, 255, 255), (self.xPos+1, self.yPos+1), (self.xPos+1, self.yPos+self.height-2))

            pygame.draw.line(self.surface, (70, 70, 70), (self.xPos+self.width-2, self.yPos+1), (self.xPos+self.width-2, self.yPos+self.height-2)) #Dark grey shadows
            pygame.draw.line(self.surface, (70, 70, 70), (self.xPos+1, self.yPos+self.height-2), (self.xPos+self.width-2, self.yPos+self.height-2))

            pygame.draw.line(self.surface, (120, 120, 120), (self.xPos+self.width-3, self.yPos+2), (self.xPos+self.width-3, self.yPos+self.height-3)) #Slightly lighter grey shadows
            pygame.draw.line(self.surface, (120, 120, 120), (self.xPos+2, self.yPos+self.height-3), (self.xPos+self.width-3, self.yPos+self.height-3))

        if self.state == "DOWN":#If the state of the mouse is down
                                #Draws the mouse button with highlights and shadows inversed, to appear like the button is pressed
            pygame.draw.rect(self.surface, (0, 0, 0), self.rect, 1) #black boarder
            pygame.draw.line(self.surface, (255, 255, 255), (self.xPos+self.width-2, self.yPos+1), (self.xPos+self.width-2, self.yPos+self.height-2)) #White highlights
            pygame.draw.line(self.surface, (255, 255, 255), (self.xPos+1, self.yPos+self.height-2), (self.xPos+self.width-2, self.yPos+self.height-2))

            pygame.draw.line(self.surface, (70, 70, 70), (self.xPos+1, self.yPos+1), (self.xPos+self.width-2, self.yPos+1)) #Dark grey shadows
            pygame.draw.line(self.surface, (70, 70, 70), (self.xPos+1, self.yPos+1), (self.xPos+1, self.yPos+self.height-2))

            pygame.draw.line(self.surface, (120, 120, 120), (self.xPos+2, self.yPos+2), (self.xPos+self.width-3, self.yPos+2))#Slightly lighter grey shadows
            pygame.draw.line(self.surface, (120, 120, 120), (self.xPos+2, self.yPos+2), (self.xPos+2, self.yPos+self.height-3))
        
        self.label = self.font.render(self.text, 1, self.textColor) #Creates text variable with the given text and color
        self.buttonRect = self.label.get_rect() #Gets the rect from the text variable
        self.buttonRect.center = self.button.center #Sets the center of the text variables rect to the center of the button
        self.surface.blit(self.label, self.buttonRect) #Renders the text to the self.surface over the button
        
    def event(self, event): #Event handeler for buttons.  Events are passed through to this function, and it checks the status of the mouse and updates the button appropriatly
        if event.type == MOUSEBUTTONDOWN: #if the type of event is a mouse click
            #if the position of the mouse is over the button
            if pygame.mouse.get_pos()[0] >= self.xPos and pygame.mouse.get_pos()[0] <= self.xPos+self.width and pygame.mouse.get_pos()[1] >= self.yPos and pygame.mouse.get_pos()[1] <= self.yPos+self.height:
                self.state="DOWN" #Changes the state of the mouse to DOWN
                self.draw() #draws the mouse with this new state
                self.play = True
                #return self.play #Play the mouse click sound
        if event.type == MOUSEBUTTONUP: #If the event type is mouse click release
            #If the position of the mouse is over the button
            if pygame.mouse.get_pos()[0] >= self.xPos and pygame.mouse.get_pos()[0] <= self.xPos+self.width and pygame.mouse.get_pos()[1] >= self.yPos and pygame.mouse.get_pos()[1] <= self.yPos+self.height:
                self.state="UP" #Change the state of the mouse to UP
                self.draw() #Draw the button with the new state
                exec(self.callback) #Execute the specified command
            else: #Else if the position of the mouse is not over the button
                self.state="UP" #Change the state to UP
                self.draw() #Draw the mouse with this new state

        if event.type == MOUSEMOTION: #If the event type is mouse motion
            #If the position of the mouse is over the button
            if pygame.mouse.get_pos()[0] >= self.xPos and pygame.mouse.get_pos()[0] <= self.xPos+self.width and pygame.mouse.get_pos()[1] >= self.yPos and pygame.mouse.get_pos()[1] <= self.yPos+self.height:
                self.hover=True #Set the hover variable to true (tells the class that the mouse is hovering over the button)
                self.draw() #Draws the mouse with the updated hover status
            else: #Else if the mouse is not over the button
                self.hover=False #Set the hover status to false
                self.draw() #draw the mouse with the updated hover status
        self.draw()

class LevelCreator:
    '''Creates individual level sections'''
    def __init__(self):
        '''Constructs class'''
        self.root=Tk()
        self.root.title("Level Creator")
        self.canvas=Canvas(self.root,width=940,height=780,background='slate grey') #Creates the LevelCreator canvas
        self.canvas.pack()
        save=Button(self.root,text="Save",command=self.save) #Creates a Save button
        exitCreator=Button(self.root,text="Exit",command=self.exitLevel) #Creates an Exit button
        clearAll = Button (self.root, text='Clear All',command = self.clear) #Creates a Clear All button
        instructions=Button(self.root,text="Instructions",command=self.instructions) #Creates an Instructions button
        load=Button(self.root,text="Load",command=self.load) #Creates an Load button
        save.pack()
        exitCreator.pack()
        clearAll.pack()
        instructions.pack()
        load.pack()
        save.place(x=30,y=530)
        exitCreator.place (x=30, y=570)
        clearAll.place (x=30,y=610)
        instructions.place(x=30,y=650)
        load.place(x=30,y=690)
        self.levelNumEntry=Entry(self.root) #Creates a Level Number entry box
        self.levelNumEntry.pack()
        self.levelNumEntry.place(x=800,y=570)
        self.levelSectionEntry=Entry(self.root) #Creates a Level Section entry box
        self.levelSectionEntry.pack()
        self.levelSectionEntry.place(x=800,y=610)
        self.loadLevelNumEntry=Entry(self.root) #Creates a Load Level Number entry box
        self.loadLevelNumEntry.pack()
        self.loadLevelNumEntry.place(x=100,y=690)
        self.loadLevelSectionEntry=Entry(self.root) #Creates a Load Level Section entry box
        self.loadLevelSectionEntry.pack()
        self.loadLevelSectionEntry.place(x=100,y=730)
        self.canvas.create_text(800,555,fill='black',font=('times',10),text="Level Number:",anchor='nw')
        self.canvas.create_text(800,595,fill='black',font=('times',10),text="Level Section:",anchor='nw')
        self.canvas.create_text(100,675,fill='black',font=('times',10),text="Load Level Number:",anchor='nw')
        self.canvas.create_text(100,715,fill='black',font=('times',10),text="Load Level Section:",anchor='nw')
        self.blockType=0
        self.orientation=0
        self.levelNum=0
        self.levelSection=0
        self.runCreator()
    def drawGrid(self):
        '''Draws level grid using Square objects'''
        self.grid=[] 
        for j in range(0,25):
            self.row=[]
            for i in range(0,45):
                square=Square(i*20,j*20,self.canvas)
                square.draw()
                self.row.append(square)
            self.grid.append(self.row)
    def legend(self):
        '''Draws a block legend using LegendSquare objects'''
        self.legend=[]
        self.canvas.create_text(260,530,text="Legend:",fill='black',font=('times',18),anchor='nw')
        #Air
        airBlock=LegendSquare(260,560,0,self.canvas)
        self.legend.append(airBlock)
        airBlock.draw()
        self.canvas.create_text(300,560,fill='black',font=('times',15),text="Air",anchor='nw')
        #Platform
        platformBlock=LegendSquare(260,580,1,self.canvas)
        self.legend.append(platformBlock)
        platformBlock.draw()
        self.canvas.create_text(300,580,fill='black',font=('times',15),text="Platform",anchor='nw')
        #Spikes
        spikeBlock=LegendSquare(260,600,2,self.canvas)
        self.legend.append(spikeBlock)
        spikeBlock.draw()
        self.canvas.create_text(300,600,fill='black',font=('times',15),text="Spikes",anchor='nw')
        #Spring
        springBlock=LegendSquare(260,620,3,self.canvas)
        self.legend.append(springBlock)
        springBlock.draw()
        self.canvas.create_text(300,620,fill='black',font=('times',15),text="Spring",anchor='nw')
        #Disapear
        disapearBlock=LegendSquare(260,640,4,self.canvas)
        self.legend.append(disapearBlock)
        disapearBlock.draw()
        self.canvas.create_text(300,640,fill='black',font=('times',15),text="Disapear",anchor='nw')
        #Death
        deathBlock=LegendSquare(260,660,5,self.canvas)
        self.legend.append(deathBlock)
        deathBlock.draw()
        self.canvas.create_text(300,660,fill='black',font=('times',15),text="Death Platform",anchor='nw')
        #Coin
        coinBlock=LegendSquare(260,680,6,self.canvas)
        self.legend.append(coinBlock)
        coinBlock.draw()
        self.canvas.create_text(300,680,fill='black',font=('times',15),text="Coins",anchor='nw')
        #Goal
        goalBlock=LegendSquare(260,700,7,self.canvas)
        self.legend.append(goalBlock)
        goalBlock.draw()
        self.canvas.create_text(300,700,fill='black',font=('times',15),text="Goal",anchor='nw')
        #Spawn
        spawnBlock=LegendSquare(260,720,8,self.canvas)
        self.legend.append(spawnBlock)
        spawnBlock.draw()
        self.canvas.create_text(300,720,fill='black',font=('times',15),text="Spawn",anchor='nw')
        #Compass
        self.canvas.create_text(540,550,fill='black',font=('times',15),text="Orientation Compass",anchor='nw')
        self.canvas.create_rectangle(600,600,601,680,fill='black')
        self.canvas.create_rectangle(560,640,640,641,fill='black')
        self.canvas.create_text(641,640,fill='black',font=('times',15),text="1",anchor='w')
        self.canvas.create_text(600,680,fill='black',font=('times',15),text="2",anchor='n')
        self.canvas.create_text(560,640,fill='black',font=('times',15),text="3",anchor='e')
        self.canvas.create_text(600,600,fill='black',font=('times',15),text="0",anchor='s')
    def runCreator(self):
        '''Runs the level creator'''
        self.drawGrid()
        self.legend()
        self.canvas.bind("<Button-1>",self.leftClick)
        self.canvas.bind("<B1-Motion>",self.leftClick)
        self.canvas.bind("<Button-3>",self.rightClick)
        self.root.mainloop()
    def leftClick(self,event):
        '''Handles left mouse button clicks on the grid/legend'''
        self.xMouse=(event.x-20)//20
        self.yMouse=(event.y-20)//20
        if self.xMouse>=0 and self.xMouse<45 and self.yMouse>=0 and self.yMouse<25: #If the left mouse button is clicked on the grid
            self.grid[self.yMouse][self.xMouse].changeType(self.blockType)
            if self.blockType==2:
                self.grid[self.yMouse][self.xMouse].changeOrientation(self.orientation)
            self.grid[self.yMouse][self.xMouse].draw()
        elif self.xMouse==12 and self.yMouse>=27 and self.yMouse<=35: #If the left mouse button is clicked on the legend
            self.position=self.yMouse-27
            for square in self.legend:
                square.reset()
            self.legend[self.position].clicked()
            self.blockType=self.legend[self.position].returnBlockType()
    def rightClick(self,event):
        '''Uses right mouse button clicks to orient certain block(s)'''
        self.xMouse=(event.x-20)//20
        self.yMouse=(event.y-20)//20
        if self.xMouse>=0 and self.xMouse<45 and self.yMouse>=0 and self.yMouse<25: #If the right mouse button is clicked on the grid
            if self.grid[self.yMouse][self.xMouse].returnBlockType()==2: #If the right mouse button is clicked on a spike block
                self.orientation+=1
                if self.orientation==4:
                    self.orientation=0
                self.grid[self.yMouse][self.xMouse].changeOrientation(self.orientation)
                self.grid[self.yMouse][self.xMouse].draw()
    def save(self):
        '''Saves the grid to a txt file'''
        self.levelNum=self.levelNumEntry.get()
        self.levelSection=self.levelSectionEntry.get()
        if self.levelNum=="":
            pass
        elif self.levelSection=="":
            pass
        elif int(self.levelNum)<=0:
            pass
        elif int(self.levelSection)<=0:
            pass
        else:
            if not os.path.exists("levels/"+"level"+str(self.levelNum)): #Checks to see if the path (directory) exists
                os.mkdir("levels/"+"level"+str(self.levelNum)) #Creates path (directory)
            self.fileName="levels/"+"level"+str(self.levelNum)+"/grid"+str(self.levelSection)+".txt"
            self.snOut=open(self.fileName,'w')
            self.snOut.write(str(int(self.levelSection)+1)+",1,"+str(int(self.levelSection)-1)+",1"+"\n")
            for i in range(0,25):
                for j in range(0,45):
                    self.snOut.write(str(self.grid[i][j].returnBlockType())+";"+str(self.grid[i][j].orientation)+",")
                self.snOut.write("\n")
            self.snOut.close()
    def load(self):
        '''Loads a previously built level'''
        #Work in progress, no clue whats wrong
        
        self.loadLevelNum=self.loadLevelNumEntry.get()
        self.loadLevelSection=self.loadLevelSectionEntry.get()
        if self.loadLevelNum=="":
            pass
        elif self.loadLevelSection=="":
            pass
        elif int(self.loadLevelNum)<=0:
            pass
        elif int(self.loadLevelSection)<=0:
            pass
        else:
            if not os.path.exists("levels/"+"level"+str(self.loadLevelNum)+"/grid"+str(self.loadLevelSection)+".txt"):
                pass
            else:
                self.fileName="levels/"+"level"+str(self.loadLevelNum)+"/grid"+str(self.loadLevelSection)+".txt"
                self.snIn=open(self.fileName,'r')
                self.grid=[]
                self.firstLine = str.strip(self.snIn.readline()) 
                for i in range(0,25):
                    self.row=str.strip(self.snIn.readline())
                    self.row=self.row.split(',')
                    self.row=self.row[0:45]
                    for j,box in enumerate(self.row): 
                        self.row[j] = box.split(';') 
                    self.grid.append(self.row)
                self.snIn.close()
                for i in range(0,25):
                    for j in range(0,45):
                        self.tempType=self.grid[i][j][0]
                        if self.tempType=='2':
                            self.tempOrientation=self.grid[i][j][1]
                        self.grid[i][j]=Square(j*20,i*20,self.canvas)
                        self.grid[i][j].changeType(self.tempType)
                        if self.grid[i][j].returnBlockType()==2:
                            self.grid[i][j].changeOrientation(self.tempOrientation)
                        self.grid[i][j].draw()
                self.levelNumEntry.delete(0,)
                self.levelSectionEntry.delete(0,)
                self.levelNumEntry.insert(0,self.loadLevelNum)
                self.levelSectionEntry.insert(0,self.loadLevelSection)                
    def instructions(self):
        '''Display instructions in a message window'''
        messagebox.showinfo("Instructions","Instructions:"+"\n"
                            "1. Select a block type from the legend"+"\n"
                            "2. Click and drag the mouse on the grid to place blocks"+"\n"
                            "3. Right click on spike blocks to rotate them according the the orietation guide on the right"+"\n"
                            "4. You may only place one spawn block per grid"+"\n"
                            "5. Place only one goal block at the very end of the level"+"\n"
                            "6. Enter the desired level number and section as integers in the entry boxes"+"\n"
                              "7. When you have finished creating the grid, click Save"+"\n"
                            "8. To load a previously built level into the creator, put the desired level number and section as integers in the 'Load' entry boxes and click the Load button"+"\n"
                              "9. Use the Clear All button to clear the grid"+"\n"
                              "10. Use the Exit button to close the window")
                            
                                              
    def exitLevel (self):
        '''Exits the level creator'''
        self.root.destroy()
    def clear (self):
        '''Clears the level grid'''
        for row in self.grid:
            for square in row:
                square.blockType=0
                square.draw()
                
                
class Square:
    '''Creates Square objects for use by the LevelCreator object grid, parent to the LegendSquare class'''
    def __init__(self,x,y,canvas):
        '''Constructs the class'''
        self.canvas=canvas
        self.xPos=x+20
        self.yPos=y+20
        self.blockType=0
        self.outline='black'
        self.orientation=""
        self.string = False
    def draw(self):
        '''Draws the Square object'''
        if self.blockType==0: #Air
            self.colour='white'
        elif self.blockType==1: #Platform
            self.colour='black'
        elif self.blockType==2: #Spikes
            self.colour='red'
        elif self.blockType==3: #Spring
            self.colour='blue'
        elif self.blockType==4: #Dispearing Block
            self.colour='dark grey'
        elif self.blockType==5: #Death Platform
            self.colour='dark red'
        elif self.blockType==6: #Coins
            self.colour='yellow'
        elif self.blockType==7: #Goal
            self.colour='cyan'
        elif self.blockType==8: #Spawn
            self.colour='green'
        else:
            self.string = True
        if self.string == False:
            if self.blockType!=2:
                self.canvas.create_rectangle(self.xPos,self.yPos,self.xPos+20,self.yPos+20,fill=self.colour,outline=self.outline,width=2)
            else:
                self.canvas.create_rectangle(self.xPos,self.yPos,self.xPos+20,self.yPos+20,fill=self.colour,outline=self.outline,width=2)
                self.canvas.create_text(self.xPos+5,self.yPos,fill='black',font=('times',15),text=str(self.orientation),anchor='nw')
        else:
            self.string = False
    def changeType(self,blockType):
        '''Changes the block type of the Square object'''
        self.blockType=blockType
        try:
            self.blockType=int(self.blockType)
        except ValueError:
            pass
    def returnBlockType(self):
        '''Returns the block type of the Square object'''
        return self.blockType
    def changeOrientation(self,orientation):
        '''Changes the orientation of the Square object'''
        self.orientation=orientation

class LegendSquare(Square):
    '''Creates Square objects for use by the LevelCreator object legend'''
    def __init__(self,x,y,blockType,canvas):
        '''Constructs the class'''
        Square.__init__(self,x,y,canvas)
        self.xPos=x
        self.yPos=y
        self.blockType=blockType
    def clicked(self):
        '''Outlines ('selects') a clicked LegendSquare object'''
        self.outline='green'
        self.draw()
    def reset(self):
        '''Redraws black outlines for an unselected LegendSquare object'''
        self.outline='black'
        self.draw()



class Block(pygame.sprite.Sprite):
    '''Parent box class'''
    def __init__(self, screen, x, y, userEvents, images):
        '''Initializes the parent block'''
        pygame.sprite.Sprite.__init__(self) # Initializes the sprite from the predefined sprite function
        self.rect = Rect(x,y,29,29) # Sets the rect for the sprite
        self.screen=screen # Imports the screen
        self.userEvents = userEvents
        self.collide=True # Makes the object collidable with
       
    def collision(self,side):
        '''Deferred method called when a collision occurs'''
        raise NotImplementedException("Subclasses are responsible for creating this method")

    def update(self):
        '''Updates the object on the screen by blitting it'''
        self.screen.blit(self.image,self.rect)


class DeathBlock(Block):
    '''The parent class for blocks that kill the player'''
    def __init__(self, screen, x, y, userEvents, images):
        '''Initializes the class'''
        Block.__init__(self, screen, x, y, userEvents, images)

    def collision(self,side):
        '''Posts the specified event when the player collides with the block'''
        pygame.event.post(pygame.event.Event(self.userEvents['PLAYER_KILL'])) # Causes the PLAYER_KILL event to run in the event loop
        
        
class Spyke(DeathBlock):##
    def __init__(self, screen, x, y, userEvents, direction, images):
        '''Initializes the class'''
        DeathBlock.__init__(self, screen, x, y, userEvents, images)
        self.rectCopy=self.rect.copy() # A copy of the original rect for the spike
        self.rect.width=27 # Reduces the rect width of the spike
        self.rect.height=27 # Reduces the rect height of the spike
        self.rect.center=self.rectCopy.center # Places the center of the new rect where the original was
        self.angle=-direction*90 # Calculates the angle value for the rotation
        self.image=images[0] # Loads the sprite image
        self.image = pygame.transform.scale(self.image, (29, 29)) # Scales the image to the correct block size
        self.image=pygame.transform.rotate(self.image,self.angle) # Rotates the image to have desired orientation
        self.type=2

    def update(self):
        self.screen.blit(self.image,self.rectCopy)


class Death(DeathBlock):##
    def __init__(self, screen, x, y, userEvents, images):
        '''Initializes the class'''
        DeathBlock.__init__(self, screen, x, y, userEvents, images)
        self.image=images[1] # Loads the sprite image
        self.image = pygame.transform.scale(self.image, (29, 29)) # Scales the image to the correct block size
        self.type=5
        

class Platform(Block):##
    def __init__(self, screen, x, y, userEvents, images):
        '''Initializes the class'''
        Block.__init__(self, screen, x, y, userEvents, images)
        self.image=images[2] # Loads the sprite image
        self.image = pygame.transform.scale(self.image, (29, 29)) # Scales the image to the correct block size
        self.type=1
        
    def collision(self,side):
        '''Prevents any action for a collision'''
        pass


class Goal(Block):##
    def __init__(self, screen, x, y, userEvents, images):
        '''Initializes the class'''
        Block.__init__(self, screen, x, y, userEvents, images) 
        self.image=images[3] # Loads the sprite image
        self.image = pygame.transform.scale(self.image, (29, 29)) # Scales the image to the correct block size
        self.type=7

    def collision(self,side):
        '''Posts the specified event when the player collides with the block'''
        pygame.event.post(pygame.event.Event(self.userEvents['LEVEL_DONE'])) # Causes the LEVEL_DONE event to run in the event loop


class BlueGoo(Block):##
    def __init__(self, screen, x, y, userEvents, images):
        '''Initializes the class'''
        Block.__init__(self, screen, x, y, userEvents, images)
        self.image=images[4] # Loads the sprite image
        self.image = pygame.transform.scale(self.image, (29, 29)) # Scales the image to the correct block size
        self.type=3

    def collision(self,side):
        '''Posts the specified event when the player collides with the block from the top only'''
        if side=='top':
            pygame.event.post(pygame.event.Event(self.userEvents['BOUNCE_GOO'])) # Causes the BOUNCE_GOO event to run in the event loop
        else:
            pass


class Spawn(Block):##
    def __init__(self, screen, x, y, userEvents, images):
        '''Initializes the class'''
        Block.__init__(self, screen, x, y, userEvents, images)
        self.image=images[5] # Loads the sprite image
        self.image = pygame.transform.scale(self.image, (29, 29)) # Scales the image to the correct block size
        self.collide=False # Makes it so the player cannot collide wit the block
        self.type=8

    def collision(self,side):
        '''Prevents any action for a collision'''
        pass


class Disappear(Block):
    def __init__(self, screen, x, y, userEvents, images):
        '''Initializes the class'''
        Block.__init__(self, screen, x, y, userEvents, images)
        self.image=images[6].convert() # Loads the sprite image
        self.image = pygame.transform.scale(self.image, (29, 29)) # Scales the image to the correct block size
        self.alpha=250 # The alpha value of the block
        self.animation=True # Prevents the animation from starting
        self.type=4

    def collision(self,side):
        self.animation=False # Trigger to start animation

    def update(self):
        '''Overwrites the update method to animate the block'''
        if not self.animation:
            if self.alpha!=0:
                self.image.set_alpha(self.alpha) # Changes the transparency of the image
                #print(self.image.get_alpha())
                self.alpha+=-4
                if self.alpha<0:
                    self.alpha=0 # Prevents the alpha from becoming negative
            else:
                self.collide=False # Prevents the block from being collidable once the animation is complete
        Block.update(self) # Calls the original update function

    def replace(self):
        '''Function to replace the blocks after they disappear'''
        self.collide=True # Makes it possible to collide with the block again
        self.animation = True
        self.alpha=250 # Restores the alpha attribute to original value
        self.image.set_alpha(self.alpha) # Sets the block back to opaque


class Coin(Block):
    def __init__(self, screen, x, y, userEvents, images):
        '''Initializes the class'''
        Block.__init__(self, screen, x, y, userEvents, images)
        self.frames=images[7] # Loads the coin .gif frame by frame
        self.frame=0 # The current frame of the image
        self.count=6 # Counter variable
        self.type=6
        

    def update(self):
        '''Owerwrite update method to animate the coin'''
        if self.collide==True:
            if self.frame==4: # Resets the frame back to the first one when loop is complete
                self.frame=0
            if self.count==6: # Changes the frame every 6 ticks
                self.image=self.frames[self.frame]
                self.count=0
                self.frame+=1
            self.screen.blit(self.image,self.rect) # Blits the image to the screen
            self.count+=1

    def collision(self,side):
        '''Posts the specified event when the player collides with the block'''
        pygame.event.post(pygame.event.Event(self.userEvents['COIN_COLLECT'])) # Causes the COIN_COLLECT event to run in the event loop
        self.collide=False # Makes it so the player cannot collide with the object anymore
        self.kill() # Removes the sprite from all groups

class Jihad (Block):
    # This class triggers a additional mode for the game called 'Jihad Mode'
    # This mode is a parody from the video game Trouble in Terrorist Town, where
    # the player can purchase a bomb, that will make them make this noise and
    # suicide bomb to kill other players. This is not intended in any other way
    # This mode may be quite annoying to some (aka it uses the noise we were told
    # not to use) so it is completely optional and will never be triggered by accident
    # It can only be triggered by hitting a special block hidden in one of the levels
    def __init__(self, screen, x, y, userEvents, images):
        '''Initializes the class'''
        Block.__init__(self, screen, x, y, userEvents, images) 
        self.image = pygame.image.load("Graphics/secrets.png")
        self.image = pygame.transform.scale(self.image, (29, 29)) # Scales the image to the correct block size

        self.type=9

    def collision(self,side):
        '''Posts the specified event when the player collides with the block'''
        self.collide=False
        pygame.event.post(pygame.event.Event(self.userEvents['JihadNoise'])) # Causes the LEVEL_DONE event to run in the event loop   

#Mainline

go = Mainclass()

