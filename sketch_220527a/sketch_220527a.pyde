import random
add_library('minim')

cannonX = 50
cannonY = 630

bulletY = 620

mode = 0

alienvx = 1
alienvy = 10

def setup():
    global alien, alienx, alieny, invasion, alienvx, alienvy, welcome_mess, abulletpos, adelaylen, abulletdelay
    global font, cannon, icon, icon2
    global welcome_bgm, shoot_bgm
    global canbulpos, bulletList
    global ascore, numLives, gameEnd, XlifeCounter, YlifeCounter
    
    size(700, 750)
    background(0)
    
    minim = Minim(this)
    welcome_bgm = minim.loadFile("intro.mp3") #Loads a sound file
    shoot_bgm = minim.loadFile("shoot.wav")
    
    welcome_mess = loadImage("welcome.png")
    cannon = loadImage("cannon.png")#laser canon
    alien = loadImage('alien2.png')
    alien.resize(30, 0)
    gameEnd = loadImage("gameover2.jpg")

    bulletList = []
    invasion = [[1 for x in range(11)] for i in range(5)]
    
    alienx = 70
    alieny = 50
    alienvx = 1
    alienvy = 10
    
    ascore = 0 # points you get from shooting aliens
    
    abulletpos = []
    
    abulletdelay = 200
    adelaylen = abulletdelay - 1
    
    numLives = 3
    XlifeCounter = 60
    YlifeCounter = 690
    

    
def draw():
    global cannon, cannonX, cannonY, mode, abulletdelay, abulletlen, adelaylen
    global canbulpos
    welcomeScreen()
    startGame()

    game_mode()

def game_mode():
    global cbullet, bulletList, ascore, abullet, abulletpos, abulletdelay, adelaylen, numLives, gameEnd
    if mode == 0:
        background(0)
        welcomeScreen()
    elif mode == 1:
        cannon_move()
        cannon_shoot()
        spawnAliens()
        movealiens()
            
        for i in range(len(bulletList)):
            cbullet(bulletList[i][0], bulletList[i][1])
            bulletList[i][1] += 8
        
        bulletList = [ pos for pos in bulletList if pos[1] < 606.25 ]
        
        if abulletdelay >= adelaylen:
            abulletdelay = 0
            alienShoot()
        
        abulletdelay += 1
        
        for i in range(len(abulletpos)):
            abullet(abulletpos[i][0], abulletpos[i][1])
            abulletpos[i][1] += 2
            
            if (abulletpos[i][0]  >= cannonX ) and (abulletpos[i][0] + 2 <= cannonX + 450/8) and (abulletpos[i][1] >= 606.25 + 10 ):
                abulletpos[i][1] = 1000
                numLives -= 1
                
        abulletpos = [ pos for pos in abulletpos if pos[1] < 606.25 + 350/8 + 10 ]
        resetAliens()
        checkforend()
        score()
        lifeDisplay()
        
    if mode == 2:
        image(gameEnd, 0, 0)
        text("Score: ", 270, 600)
        text(ascore, 360, 600)
        text("Press r to play again", 200, 650)
        
        
def spawnAliens():
    global alienx, alieny, alien, invasion, alienvx, ascore
    
    # generate aliens
    for row in range(len(invasion[0])):
        for col in range(len(invasion)):
            if invasion[col][row] == 1:
                image(alien, alienx + row * 50, alieny + col * 40)
                
                for i in range(len(bulletList)):
                    if ((606.25 - bulletList[i][1] < (alieny+col * 40)) and (606.25 - bulletList[i][1] > (alieny+col * 40 - 22.4))) and ((bulletList[i][0] - 2.5 > alienx + row * 50 and bulletList[i][0] -2.5 < alienx + row * 50+30) or (bulletList[i][0] + 2.5 > alienx + row * 50 and bulletList[i][0] + 2.5 < alienx + row * 50+30)) :
                        
                        # removes bullet that hit an alien
                        bulletList[i][1] = 900

                        invasion[col][row] = 0 
                        ascore += 5    
    alienx += alienvx
    
def startGame(): #checks if s is pressed ->start game
    global cannonX, cannonY, mode
    if mode == 0:
        if (keyPressed) and (key == 's'):
            mode = 1

def reset():
    global numLives, ascore, abulletpos, cannonx, mode, invasion, alienx, alieny, alienvx, alienvy
    numLives = 3
    ascore = 0
    abulletpos = []
    cannonx = 0
    mode = 0
            
    invasion = [[1 for x in range(11)] for i in range(5)]
    alienx = 70
    alieny = 50
    alienvx = 1
    alienvy = 10
    

    
def movealiens():
    global alienvx, alienvy, alienx, alieny, invasion 
    #fn to move the aliens 

    for row in range(len(invasion[0])):
        for col in range(len(invasion)):
            
            if invasion[col][row] == 1:
                if alienx+row*50 + 30 > width:
                    alienvx *= -1
                    alieny += alienvy
                    break
            
                if alienx+row*50 < 0:
                    alienvx *= -1
                    alieny += alienvy
                    break
                    
                if alieny + col * 40 + 22.4 > 606.25:
                    alienvy = 0

def alienShoot():
    global abullet, abulletpos

    exposedAliens = []

    colAliens = []

    for col in range(len(invasion[0])):
        for row in range(len(invasion)):
            colAliens.append(invasion[row][col])
            
        if 1 in colAliens:
            bottomAlien = [len(colAliens) - 1 - colAliens[::-1].index(1), col]
            exposedAliens.append(bottomAlien)
            
        colAliens = []
        
    activeAlien = random.choice(exposedAliens)

    abulletpos.append([alienx + activeAlien[1] * 50 + 15, alieny + activeAlien[0] * 40 + 22.4])

    
    
def abullet(x, y):
    fill(255)
    stroke(255)
    rect(x - 2.5, y, 2, 10)     
    


def alientBullet(x, y):
    fill(255)
    stroke(255)
    rect(x, 606.25 - y, 5, 15)  

    
def create_bullet(x,y):
    global cannonX, cannonY, bulletY
    bulletList.append([cannonX+28.125, 0])
        
def keyPressed():
    global cannonX, shoot_bgm, mode
    if mode == 1:
        if key == " " :
            create_bullet(cannonX + 45, 620)
            bulletList.append([cannonX+28.125, 0])
    if mode == 2 and key == "r":
        reset()
    
def cannon_shoot():
    global cannonX, cannonY, bulletY
    global canbulpos
    global shoot_bgm


def cbullet(x, y):
    global cannonX, cannonY
    fill(255)
    stroke(255)
    rect(x, 606.25 - y, 5, 15)
    
def cannon_move(): #the movement of the cannon
    global cannon, cannonX, cannonY
    background(0)
    if (key == CODED) and (keyPressed): #True if the key is coded and False otherwise
        if (keyCode == LEFT) and cannonX > -10: #going left
            cannonX -= 3
        elif (keyCode == RIGHT) and cannonX < 660:#going right
            cannonX += 3
    image(cannon, cannonX, 606.25, 450/7, 350/7)
         
def welcomeScreen():
    global welcome_mess
    image(welcome_mess, 0, 0, 700, 750)
    
def resetAliens():
    global numLives, abulletpos, invasion, alienx, alieny, alienvx, alienvy
    resetPoints = ascore%550
    print(resetPoints)
    if resetPoints== 0:
        abulletpos = []
        invasion = [[1 for x in range(11)] for i in range(5)]
        alienx = 70
        alieny = 50
        alienvx = 1
        alienvy = 10
        
def score():
    global ascore
    textSize(20)
    text("Score", 40, 40)
    text(ascore, 100, 40)
        

def checkforend():
    global mode, invasion, alieny, numLives, alienvy, won, ascore
    if mode == 1:
        for row in range(len(invasion[0])):
            for col in range(len(invasion)):
                if invasion[col][row] == 1:
                    if alieny + col * 40 + 22.4 > 606.25 or numLives == 0:
                        mode = 2
                        
def lifeDisplay():
    global numLives, XlifeCounter, YlifeCounter
    textSize(30)
    text("{}".format(numLives), XlifeCounter, YlifeCounter + 35)
    
    for life in range(numLives):
        image(cannon, XlifeCounter + 50 + life*65, YlifeCounter, 450/8, 350/8) #resizes cannon to one eight its orignal size and places it at the right spot 
