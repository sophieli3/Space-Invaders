add_library('minim')

cannonX = 50
cannonY = 630

bulletY = 620

mode = 0

alienvx = 1
alienvy = 10

def setup():
    global alien, alienx, alieny, invasion, alienvx, alienvy, welcome_mess
    global font, cannon, icon, icon2
    global welcome_bgm, shoot_bgm
    global canbulpos, bulletList
    global ascore
    
    size(700, 750)
    background(0)
    
    minim = Minim(this)
    welcome_bgm = minim.loadFile("intro.mp3") #Loads a sound file
    shoot_bgm = minim.loadFile("shoot.wav")
    
    welcome_mess = loadImage("welcome.png")
    cannon = loadImage("cannon.png")#laser canon
    alien = loadImage('alien2.png')
    alien.resize(30, 0)

    bulletList = []
    invasion = [[1 for x in range(11)] for i in range(5)]
    
    alienx = 70
    alieny = 50
    alienvx = 1
    alienvy = 10
    
    ascore = 0 # points you get from shooting aliens
    
def draw():
    global cannon, cannonX, cannonY, mode
    global canbulpos
    welcomeScreen()
    startGame()

    game_mode()

def game_mode():
    global cbullet, bulletList, ascore
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
                        ascore += 10    
                        print(ascore)
    alienx += alienvx
    
def startGame(): #checks if s is pressed ->start game
    global cannonX, cannonY, mode
    if (keyPressed) and (key == 's'):
        mode = 1

    
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
    
    
    

    
