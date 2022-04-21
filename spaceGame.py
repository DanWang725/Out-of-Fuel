### The game first will initialize the empty/important variables the will be needed for the player's stuff. After that, there are
### the functions the are initialized, this way, if I forget to use global in a function, the variables that it would most likely use would
### be declared above, meaning there are no issues. After that is the initialization of the images/text and all of the arrays of Rects 
### for each game state.

from pygame import * #pygame template   
import math
import os
import random
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)

init()

#fon = font.get_fonts()
#fon.sort()
#for word in fon:
#    print(word)
    

RED = (255, 0, 0)
LIGHTRED = (255,204,204)
DARK_RED = (139,0,0)
BLACK = (0,0,0)
RED = (255, 0, 0)
BLACK = (30,30,30)
MOREBLACK = (0,0,0)
YELLOW = (255,255,0)
MUTED_YELLOW = (202,209,73)
WHITE = (255,255,255)
LESS_WHITE = (240,240,240)
BLUE = (0,0,255)
LESSBLUE = (40,40,255)
LIGHTBLUE = (100,100,255)
LIGHT_GREY = (180,180,180)
GREY = (150,150,150)
DARKLIGHT_GREY = (125,125,125)
DARK_GREY = (100,100,100)

SIZE = (1000, 700)
flags = DOUBLEBUF
screen = display.set_mode(SIZE,flags)
fpsClock = time.Clock()

gameState = 0                   #the main state of the game
subGameState = 0                #decides which menu in open in that state of the game
keysActive = [0,0,0,0,0,0,0,0,0] #list for which keys are pressed, in this order: W,S,A,D,Q,E,ESC
keyCode = [119,115,97,100,113,101,27] #the key id for each key, in the same order as the list above

saveFileIndex = "" #the index of the save file that the player is currently playing on
saveFileList = ["src/playerData/save1.dat","src/playerData/save2.dat","src/playerData/save3.dat"]
saveNameList = []
isSaveEmptyList = []


click = False           #if the mouse was clicked, this turns to True
needKey = False         #if all of the key presses are needed for something
keyPressed = []         #list of keys pressed (any key)
textBox = ""            #storing anything the player typed
mouseInfo = []

leaderBoards = []#the list that contains the leaderboard entries
pIndex = 11 #QOL, the player's current score is stored here so on the leaderboard they know where they were

pName = ""
pHealth = 100           #the health of the player

pThrustPower = 0.5        #the power of the main thrust (pressing W)
pSidePower = 0.2        #the power of the side thrusters (pressing ASD)

pDir = 0                #the direction the player is facing
pVelX = 0               #the movement of the player on the x axis
pVelY = 0               #the movement of the player on the y axis
pChangeX = 0        #the temporary force on the x axis (these store the thrust's vel for that frame)
pChangeY = 0        #the temporary froce on the y axis 
pHitboxFront = ""       #stores the coordinates for the front hitbox
pHitboxBack = ""        #stores the coordinates for the back hitbox

pBrake = 1.05       #the divider for slowing down
pRotation = 0.5       #how fast the ship rotates

pCapacity = 10
pRange = 100
pCurrentCapacity = 0
pCollectNum = 0
pStatus = True
isAcceptedWin = False

isDeleteSaveFile = False

pStoredFuel = 0
pStoredEnergy = 0
pTime = 0
pDeaths = 0
pCollectedTotal = 0
pEnergyTotal = 0

pConvertAmount = 0

pQueueList = []         #the queue for drawing thrust
shipPartList = [0,0,0,0,0,0]       #the array for the current ship images (needed for when upgrades apply)
shipPartListLarge = [0,0,0,0,0,0]
shipPartListSelect = [0,0,0,0,0]
shipAtBaseRect = [0,0,0,0,0]
shipPartUpgradedList = [0,0,0,0,0] #the array that stores if the ship's part is upgraded or not
shipPartRotate = []     #the array storing the rotated images of the ship

baseUpgraded = [0,0,0,0]

gameTimer = 0

upgradeNameList = []
upgradeDescList = []
upgradeEffectList = []
upgradeCostList = []

rectList = []
rectImages = []
rectAction = []

upgradeLabelRectList = [(150,250),(220,500),(600,200),(700,490),(850,400)]
partLoc = [(332,350),(362,350),(530,350),(632,350),(590,350)]


pStartTime = 0
pPointsTotal = 0
pTimeSincePoints = 0
pPointGameQuick = 2000
pPointCollectQuick = 5000
upgradeChance = 10 #the variable of the chance to get hydrogen asteroids
astSpeedMult = 1

astBackground = []
astRectBack = []
needChangeX = 0
needChangeY = 0

difficultySetting = 8
astListVel = []
astListSize = []
astListImg = []
astListType = []
astListRect = []
astToBeRemoved = []

avalAstImage = []
avalAstHydImage = []

fuelCollect = 0

###################################### Functions #####################################################

def estFont(fon,siz):                   #function for creating font objects
    fontWord = font.SysFont(fon,siz)    #creating the font 
    return fontWord                     #returns the objecct

def renderText(fontObj,word,col):       #function to create the text surface render
    text = fontObj.render(str(word),1,col)   #making the render from the word send and colour
    return text                         #returning the variable
    
def splitForceComp(pDir,power):         #gets the change in x and y values
    if pDir < 90:                      #this would be a regular right angle triangle, so nothing needs to be changed 
        pRad = math.radians(pDir)       #converts the angle to radians, because the math module equates in radians.
        xDisp = power * math.cos(pRad)  #the standard arm is on the x-axis, so adjacent value from angle is the x axis.
        yDisp = power * math.sin(pRad)  #sine is used here because it is the opposite value
    elif pDir >= 90 and pDir < 180:     #the second quadrant
        pRad = math.radians(pDir-90)    #remove 90 from the angle
        xDisp = -(power * math.sin(pRad)) #the x value would be negative, so after the calculation, it becomes negative
        yDisp = power * math.cos(pRad)  #The y-value is calculated with sin this time, because it is rotated compared to the original angle.
    elif pDir >= 180 and pDir < 270:    #the third quadrant
        pRad = math.radians(pDir-180)   #180 is subtracted from the angle, to make it a 90 degree right triangle
        xDisp = -(power * math.cos(pRad)) #both the x and y values are going to be negative, because it is opposite on both
        yDisp = -(power * math.sin(pRad)) #axises compared to the original 90 degree angle.
    else:                               #the forth quadrant (270 - 360 degrees)
        pRad = math.radians(pDir-270)   #270 is subtracted from the degrees to make it 90 degrees and less.
        xDisp = power * math.sin(pRad)  #cosine and sin are once again switched around
        yDisp = -(power * math.cos(pRad)) 
        
    return xDisp,yDisp              #returning the 2 values
    
def getAngleChange(direction,angleSub): #subtracts an angle from the original angle to get desired angle
    newAng = direction - angleSub
    if newAng < 0:                  #detecting if the angle is below 0, not a valid degrees.
        newAng + 360                #if it is, then add 360 to it.
    return newAng               #returns angle


#this was not made by me, was taken from : 
#https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame/54714144

def rot_center(image, angle,moveCoords):

    center = image.get_rect().center    #getting the center of original image
    rotated_image = transform.rotate(image, angle) #rotates the image
    new_rect = rotated_image.get_rect(center = center)#makes a new rectangle with the same center as the original one
    new_rect = new_rect.move(moveCoords) #moves it to the desired coords
    return rotated_image, new_rect #returns the image and rectange

def getPartLoc(coord,orbitLoc,pDir):                    #gets the location of a ship part according to angle
    x,y = coord[0] - orbitLoc[0],coord[1]-orbitLoc[1]   #getting the x and y to get distance from rotation point
    radius = math.sqrt(x*x+y*y)                         #calculating the radius
    pRad = math.radians(pDir)                           #converting the angle from degrees to radians
    
    finalX = orbitLoc[0] - (radius * math.cos(pRad))    #uses trigonometry to find the coordinates of the part
    finalY = orbitLoc[1] + (radius * math.sin(pRad))
    return finalX,finalY
    
def getAlteredImage(image,anchorCoord,loc):             #function that justifies the image rectangle
    imgRect = image.get_rect()                          #gets the specifications of the image
    if loc == "center":                                 #deciding how to position an image
        newRect = Rect(anchorCoord[0]-imgRect.width/2,anchorCoord[1]-imgRect.height/2,imgRect.width,imgRect.height) #generates the rectangle
        #for the image with the coordinate in the centre of the coordinates
    elif loc == "right":                                #if the image needs to be anchored with the right side on the coord
        newRect = Rect(anchorCoord[0]-imgRect.width,anchorCoord[1],imgRect.width,imgRect.height)
    elif loc == "left":                                 #if the image needs to be anchored with the left side on the coord
        newRect = Rect(anchorCoord[0],anchorCoord[1],imgRect.width,imgRect.height)
    elif loc == "right_center":
        newRect = Rect(anchorCoord[0]-imgRect.width,anchorCoord[1]-imgRect.height/2,imgRect.width,imgRect.height)
    return newRect                                      #returning the rect
    
def getShortenedPower(powerValue):          #function that shortens and adds the correct unit for a value of power
    powerValue = int(powerValue)
    if powerValue < 1000:                   #if the value is below 1000 MW
        energyString = str(powerValue)+"MW" #typecast the int, and add MW to the end
    elif powerValue < 1000000:              #if the value is below 1,000,000 MW
        energyString = str(powerValue)      #the value is going to be in GW, because if it was below 1 GW, it would pass through the first
        #print(energyString)
        energyString = energyString[:-3]+"."+energyString[-3]+"GW" #removes the 3 digits in the back, and takes the 3rd digit for decimal
    elif powerValue >= 1000000:
        energyString = str(powerValue)
        energyString = energyString[:-6]+"."+energyString[-6]+"TW"
    return energyString                     #return a string
    
    
    
def checkCircleCollision(circle1,circle2,radius1,radius2):          #checking the collision between two circles
    circleDist = math.sqrt((circle1[0]-circle2[0])**2 + (circle1[1]-circle2[1])**2) #does the entire equation in 1 line
    if circleDist < radius1+radius2:    #detecting if distance is smaller than the two radiuses 
        return True                     #returns boolean
    else:
        return False
    
def detectOffScreen(imageRect,offset): #detects if the rect is completely off the screen
    if imageRect.top > 700 + offset: #if the top of the image is below the screen
        #print("Top:",imageRect.top)
        return 0,1 #returns that the x needs no change, the y is over (means 1)
    elif imageRect.bottom < 0 - offset:
        #print("Bottom:",imageRect.bottom)
        return 0,-1 #-1 for the y change means that it is under (in the negative coordinates)
    elif imageRect.left > 1000 + offset: #if the left side is beyond the right side of the screen
        #print("Left:",imageRect.left)
        return 1,0
    elif imageRect.right < 0 - offset:
        #print("Right:",imageRect.right,"Left:",imageRect.left)
        return -1,0
    else:
        return 0,0


def getDir(loc,target): #gets the direction of where the objecct is heading
    deltaX = loc[0] - target[0]         #gets the change in x and y values between the target and location
    deltaY = loc[1] - target[1] 
    if deltaX > 0:                      #if the x value is positive (quadrant 1 and 4)
        if deltaY > 0:                  #if the y value is also positive (means quadrant 1)
            angResult = math.degrees(math.atan(deltaY/deltaX)) #uses inverse tan to find the angle
        elif deltaY < 0:                #if the y value is negative (quadrant 4)
            angResult = 360-math.degrees(math.acos(deltaX/(math.sqrt(deltaX*deltaX+deltaY*deltaY)))) #uses the CAST rule to find the angle
        else:                               #if the value is equal to 0                              and uses inverse of cosine,
            angResult = 0
    elif deltaX < 0:                    #if the x value is below 0 (quadrants 2 and 3
        if deltaY > 0:                  #if the y value is above 0
            angResult = 180-math.degrees(math.asin(deltaY/math.sqrt(deltaX*deltaX + deltaY*deltaY))) #uses inverse sine, and gets the 
        elif deltaY < 0:                #if the y value is below 0 (quadrant 3)                      #hypotenuse in the equation
            angResult = 180+math.degrees(math.atan(deltaY/deltaX))  #will use inverse of tan, and gets 180 added to it to get the real angle
        else:                           #if the y value is 0
            angResult = 180
    else:                               #if the x value is 0
        if deltaY > 0:                  #if the y value is greater than 0
            angResult = 90              #means that it would be at 90 degrees
        else:                           #the only other option is for it to be negative, both can't be 0 due to the generation of locations
            angResult = 270
    return angResult #returns the result
            
            
def adjustSize(image,size):             #small function for resizing the image
    newImage = transform.scale(image,(size*2,size*2))       #takes the image and makes it the specified width and height
    return newImage
    
def genAst():
    global astListVel,astListType,astListSize,astListImg,astListRect,upgradeChance,astSpeedMult #uses global to access these lists
    #the loc is generated by having 2 sets of cordinates generated, one at the edge of the x axis, and the other for the y.
    loc = random.choice([(random.randint(-200,1200),random.choice([-300,800])),(random.choice([-300,1200]),random.randint(-200,800))]) 
    vel = random.randint(3,5)*astSpeedMult                       #velocity is randomly generated
    target = (random.randint(0,1000),random.randint(0,700))#generates the coordinates of a place on the screen, ensures 
    direction = getDir(loc,target)             #gets the angle that the asteroid is travelling          that it will appear on screen
    forceComponenets = splitForceComp(direction,vel)    #Gets the x and y values of the direction travelling
    astType = random.randint(1,upgradeChance)           #Deciding the chance that a hydrogen asteroid is spawned, number is reduced by upgrade
    if astType == 1:                                    #if it gets 1, the  the asteroid is a hydrogen one
        astSize = random.randint(10,20)                 #generates the size of the asteroid
        astListType.append(True)                        #marks on the array that it will be a special asteroid
        astImg = random.choice(avalAstHydImage)         #chooses an image for it to be
    else:                                   #if the asteroid is normal
        astSize = random.randint(30,70)                 #generates the size, these will be larger
        astListType.append(False)                       #marks in the array that it will not be special
        astImg = random.choice(avalAstImage)            #chooses an image
    newImage = adjustSize(astImg,astSize)               #sends the image to a function that resizes it
    rectangle = Rect(loc[0], loc[1], newImage.get_rect().width, newImage.get_rect().height)#creates a rectangle object that is same as image
    astListSize.append(astSize)                     #these send each variable to the correct array
    astListImg.append(newImage)
    astListRect.append(rectangle)
    astListVel.append(forceComponenets)

def removeAstFromList(index,allAst):    #function that removes an ast from all of the relevant lists
    global astListVel,astListType,astListSize,astListImg,astListRect #uses global to access these lists
    if allAst:                          #a bool for if all of them are going to be cleared
        astListVel.clear()
        astListType.clear()
        astListSize.clear()
        astListImg.clear()
        astListRect.clear()
    else:                               #just removing 1 entry from the list
        astListVel.pop(index)           #pop clears the entry and shifts the index for all of them forward, so there is no 
        astListType.pop(index)          #empty spaces inbetween them.
        astListSize.pop(index)
        astListImg.pop(index)
        astListRect.pop(index)
     
def buildShipParts():                                               #adds the images for each ship part depending on the upgrade level
    global shipPartList,shipPartListLarge,shipPartUpgradedList,shipPartListSelect      #accessing the arrays for the images
    global circleTemp,circleArea,circleAreaRect,pRange

    for x in range(5):                                              #looping for each ship part
        if shipPartUpgradedList[x]:                                 #1 = true in bool, so it is faster comparison
            fileName = "assets/upgrade"+str(x+1)+"b.png"            #all images start with upgrade, then have the number and level
            fileNameL = "assets/upgrade"+str(x+1)+"bL.png"
            fileNameLSelect = "assets/upgrade"+str(x+1)+"bLSelect.png"
        else:                                                       #if the ship part is not upgraded
            fileName = "assets/upgrade"+str(x+1)+"a.png"            #the stock parts are identified with the upgrade a
            fileNameL = "assets/upgrade"+str(x+1)+"aL.png"          #getting the image for the large (hub menu) version
            fileNameLSelect = "assets/upgrade"+str(x+1)+"aLSelect.png"  #Getting the highlighted version
            
        shipPartList[x+1] = image.load(fileName).convert_alpha()                    #replacing the old image with the new one
        shipPartListLarge[x+1] = image.load(fileNameL).convert_alpha()              #replacing the old large image with the newer one
        shipPartListSelect[x] = image.load(fileNameLSelect).convert_alpha()         #replacing the old highlighted image with the new one
        
    circleArea = adjustSize(circleTemp,pRange)
    circleAreaRect = getAlteredImage(circleArea,(500,350),"center")
        
def upgradeStat(index):                             #upgrades a stat of the player ship
    global pThrustPower,pSidePower,pRotation,upgradeChance,pCapacity,pRange    #accessing global variable for each stat
    
    if index == 0:      #if the index is 0, it is the first part, meaning the main thrusters
        pThrustPower += 0.5
    elif index == 1:    #rotation thrusters
        pRotation += 3
    elif index == 2:    #fuel tanks
        pCapacity += 5
        pRange = 200
    elif index == 3:    #reverse thrusters
        pSidePower += 0.5
    elif index == 4:    #radar
        upgradeChance = 7
    
def loadSaveFile(file,extentOfLoad):        #function for loading save files
    global pName, pHealth,pThrustPower,pSidePower,pRotation,pCapacity,upgradeChance,pDeaths,pCollectedTotal,pEnergyTotal
    global shipPartUpgradedList,baseUpgraded, pStoredFuel,pStoredEnergy,pRange,isAcceptedWin
    
    saveFile = open(file,"r")               #opens the file
    if extentOfLoad == 0:                   #if just the name is needed, then read 1 line only
        name = saveFile.readline().rstrip("\n") #reads the first line, which is just the name
        saveFile.close()
        return name 
    elif extentOfLoad == 1:                             #if the whole file needs to be read, then run this
        pName = saveFile.readline().rstrip("\n")        #saves the name to the variable
        
        upgradesShip = saveFile.readline().rstrip("\n").split(",")   #gets the line containing the level of upgrade for the player's ship
                         #splits the numbers by the comma
        for x in range(len(upgradesShip)):              #replaces the parts in the lists with the new data
            shipPartUpgradedList[x] = int(upgradesShip[x])
        
        upgradesBase = saveFile.readline().rstrip("\n").split(",")   #takes the next line in the save, which is the base upgrades
                         #splits the data by the comma
        for x in range(len(upgradesBase)):              #handling the boolean and putting it into the array of base upgrade levels
            baseUpgraded[x] = int(upgradesBase[x])        
            
        genData = saveFile.readline().rstrip("\n").split(",")        #reading the next line, which is general player stats
         #splitting the data by commas
        pHealth = int(genData[0])                       #getting and assigning all of the data to the correct variable
        pThrustPower = float(genData[1])                #these need to be float due to the smaller values
        pSidePower = float(genData[2])
        pRotation = int(genData[3])
        pCapacity = int(genData[4])
        pRange = int(genData[5])
        upgradeChance = int(genData[6])
        pStoredFuel = int(genData[7])
        pStoredEnergy = int(genData[8])
        
        miscData = saveFile.readline().rstrip("\n").split(",")       #the last line contains player stats, not that important
        pDeaths = int(miscData[0])
        pCollectedTotal = int(miscData[1])
        pEnergyTotal = int(miscData[2])
        saveFile.close()
        isAcceptedWin = False
        return 0
        ###how a save file is formatted:
        #name
        #1,1,1,1,1               #these are the upgraded parts
        #1,1,1,1                 #upgrades for the base
        #100,1.0,0.2,5,10,12,0,0        #starting from left: health, main thrust, back thrust, rotation speed, holding capacity, asteroid chance
        #0,0,0                   #some stats that are stored: deaths,asteroid collected,total energy generated
        
def updateSaveFile(file):       #writing the new data for the save file
    global pName, pHealth,pThrustPower,pSidePower,pRotation,pCapacity,upgradeChance,pDeaths,pCollectedTotal,pEnergyTotal
    global shipPartUpgradedList,baseUpgraded,pStoredFuel,pStoredEnergy,pRange
    
    firstLine = pName + "\n"    #the first line is just the name of it
    
    secondLine = ""             #second line is initialized as empty string
    for upgrade in shipPartUpgradedList:        #adds all of the ship upgrades, separated by commas
        secondLine = secondLine + str(upgrade) + ","
    secondLine = secondLine[:-1]+"\n"           #removes the last comma and adds a break to the end
    
    thirdLine = ""
    for upgrade in baseUpgraded:
        thirdLine = thirdLine + str(upgrade) + ","
    thirdLine = thirdLine[:-1]+"\n"
    
    fourthLine = str(pHealth)+","+str(pThrustPower)+","+str(pSidePower)+","+str(pRotation)+","+str(pCapacity)+","+str(pRange)+","+str(upgradeChance)+","+ str(int(pStoredFuel))+","+str(int(pStoredEnergy))+"\n"
    fifthLine = str(pDeaths)+","+str(int(pCollectedTotal))+","+str(int(pEnergyTotal))+"\n"
    
    saveFile = open(file,"w")
    saveFile.write(firstLine+secondLine+thirdLine+fourthLine+fifthLine)
    saveFile.close()

def deleteSaveFile(file):               #function for deleting a save file
    saveFile = open(file,"w")           #opening the file in write mode
    saveFile.write("Empty")             #the word empty on the first line is all it needs
    saveFile.close()                    #closes the file
    
def rebuildSaveFileArray():
    global isSaveEmptyList,saveNameList,saveFileList
    
    isSaveEmptyList.clear()
    saveNameList.clear()
    
    for save in saveFileList:                                   #goes through each save file and gets the name
        saveName = loadSaveFile(save,0)                         #calls the function, setting it to only read the name
        saveNameList.append(saveName)                           #pushes the name to the list
        if saveName == "Empty":                                 #checks to see if the save file is empty
            isSaveEmptyList.append(True)                        
        else:
            isSaveEmptyList.append(False)    
    
def loadLeaderboards():                 #function to load the leaderboards
    global leaderBoards                 #accessing the global variable list
    rankings = open("src/leaderboards.dat","r") #openning the file that contains leaderboards
    leaderBoards = rankings.readline().split("~")       #the info is all on 1 line, so it takes it and splits it by ~ character
    for x in range(len(leaderBoards)):                  #goes through all the data in the list
        leaderBoards[x] = leaderBoards[x].split(",")    #all of the data still need to be split into tuples, by the , between them
    #print(leaderBoards)
    rankings.close()                                    #closes the file
    
def updateLeaderboards(currPoints,pName):           #file that takes in and writes the new leaderboards
    global leaderBoards                             #accessing the global variable
    pIndex = 11                                     #setting the index to higher than the leaderboards, incase the score doesn't get on it
    #print(len(leaderBoards))                        
    if currPoints >= int(leaderBoards[9][1]):       #checks if the score is higher than the lowest one
        for x in leaderBoards:                      #if it is, then goes through each score and compares, is not efficient as other searches
            if currPoints >= int(x[1]):             #comparing scores
                pIndex = leaderBoards.index(x)      #finds the index of where the score will be
                leaderBoards.insert(pIndex,(pName,currPoints))      #inserts the new score, all scores behind it get moved back
                leaderBoards.pop()                  #removes the last item on the list, it is not high anymore
                break
    lineToSendToFile = ""               #init an empty variable
    for x in range(10):                 #goes through the 10 leaderboard entries
        lineToSendToFile += leaderBoards[x][0]+","+str(leaderBoards[x][1])+"~" #adds the current entry, with the , and ~ dividers
    lineToSendToFile = lineToSendToFile[:-1]        #removes the last character, (~) because it might cause problems
    #print(lineToSendToFile)                         
    rankings = open("src/leaderboards.dat","w")     #opens the file, this time is writing mode
    rankings.write(lineToSendToFile)                #writes the 1 line
    rankings.close()                                #closes the file
    return pIndex                           #returns the index of the player's position on the leaderboard
        
def loadUpgrades():     #loading all upgrade for parts from a file
    global upgradeNameList,upgradeDescList,upgradeCostList,upgradeEffectList
    fileLoad = open("src/upgradeCosts.dat","r") #opening the file
    for line in fileLoad.readlines():           #reads through all of the lines
        line = line.rstrip("\n").split(",")     #splits each line by the comma
        upgradeNameList.append(line[1])         #the first index (0) is ignored, the second data, (index 1) contains the name
        upgradeDescList.append(line[2])         #index 2 contains the description
        upgradeEffectList.append(line[3])       #index 3 contains the effect of the upgrade
        upgradeCostList.append(int(line[4]))    #index 4 contains the cost, so it is typecasted
    fileLoad.close()                            #file is closed
    
def resetPlayerStats(): #resets all of the relevant stats for the main game
    global pStartTime,pPointsTotal,pTimeSincePoints,pVelX,pVelY,pDir,pHealth,difficultySetting,textBox,astSpeedMult
    
    pStartTime = 0
    pPointsTotal = 0
    pTimeSincePoints = 0
    pVelX = 0
    pVelY = 0
    pDir = 0
    difficultySetting = 8
    astSpeedMult = 1
    removeAstFromList(0,1)
    textBox = ""
    
def getAllStats():
    
    global pName, pHealth,pThrustPower,pSidePower,pRotation,pCapacity,upgradeChance,pDeaths,pCollectedTotal,pEnergyTotal
    
    stat1 = renderText(fontDev,str(pHealth),WHITE)
    stat2 = renderText(fontDev,pThrustPower,WHITE)
    stat3 = renderText(fontDev,pSidePower,WHITE)
    stat4 = renderText(fontDev,pRotation,WHITE)
    stat5 = renderText(fontDev,pCapacity,WHITE)
    stat6 = renderText(fontDev,upgradeChance,WHITE)
    stat7 = renderText(fontDev,pDeaths,WHITE)
    stat8 = renderText(fontDev,pCollectedTotal,WHITE)
    stat9 = renderText(fontDev,pEnergyTotal,WHITE)
    screen.blit(stat1,getAlteredImage(stat1,(50,50),"center"))
    screen.blit(stat2,getAlteredImage(stat2,(50,75),"center"))
    screen.blit(stat3,getAlteredImage(stat3,(50,100),"center"))
    screen.blit(stat4,getAlteredImage(stat4,(50,125),"center"))
    screen.blit(stat5,getAlteredImage(stat5,(50,150),"center"))
    screen.blit(stat6,getAlteredImage(stat6,(50,175),"center"))
    screen.blit(stat7,getAlteredImage(stat7,(50,200),"center"))
    screen.blit(stat8,getAlteredImage(stat8,(50,225),"center"))
    screen.blit(stat9,getAlteredImage(stat9,(50,250),"center"))
    

################################################# variable creation ##########################################################
    
    
    

fontMainMenu = estFont("tahoma",70) #loading all the fonts used for the game
fontButton = estFont("corbel",45) #font for buttons
fontButtonSelect = estFont("corbel",50) #font for highlighted buttons
fontInfo = estFont("verdana",22)
#fontInfo = estFont("corbel",25)
fontDev = estFont("lucidaconsole",10)

#loading all of the text that will be used
mainMenuTitle = renderText(fontMainMenu,"Out of Power",WHITE)

buttonStart = renderText(fontButton,"Start",WHITE)
buttonHelp = renderText(fontButton,"Help",WHITE)
buttonQuit = renderText(fontButton,"Quit",WHITE)

buttonStartE = renderText(fontButtonSelect,"Start",WHITE)
buttonHelpE = renderText(fontButtonSelect,"Help",WHITE)
buttonQuitE = renderText(fontButtonSelect,"Quit",WHITE)


#the rect list for drawing the information text
helpScreenRectList1 = [(70,100),(100,200),(140,250),(100,300),(140,340),(140,370),(140,400),(100,450),(140,490),
                      (140,520),(140,550)]
helpScreenTextList1 = ["How to Play","Objectives","Dodge Asteroids and E Waste While Collecting Fuel/Points",
                      "General Controls","Press W to go forward, Sto move backward","Use the A and D keys to rotate your ship",
                      "Press Esc to leave exit the help screen","Collecting Special Asteroids:",
                      "Apart from normal asteroids you have to dodge, there will be special",
                      "ones that you need to collect by clicking on them. These will",
                      "be brighter and smaller compared to the e-waste and asteroids"]
helpScreenRectList2 = [(70,100),(100,200),(130,250),(130,280),(130,310),(130,340),(130,380),(130,410),(110,460),
                      (130,510),(130,540),(130,570)]
helpScreenTextList2 = ["How to Play cont.","Story Mode: Lore",
                      "The computers on Earth have become very essential in developing",
                      "new technology during this time. However, they consumed exponentially",
                      "more power compared to 2020's computers. The fuel sources on Earth",
                      "are now at critical levels, and are now only to be used for emergencies",
                      "That's where you come in. Thankfully, before everything shut down,",
                      "remotely guided space drones were completed.","Objective:",
                      "It is your job to fly into asteroid fields, and gather hydrogen",
                      "Once you get enough fuel, you will be able to power up some computers",
                      "You will be able to research/equip technology that will help you."]        
helpScreenRectList3 = [(70,100),(100,200),(130,250),(130,280),(130,320),(130,350),(100,390),(130,440),(130,470),(130,500),
                       (130,530),(130,560)]    
helpScreenTextList3 = ["How to Play...3","Story Mode: Other Helpful Things:",
                       "You have to be a certain range from special asteroids to be able",
                       "To collect it, indicated with the white circle around your ship",
                       "You are able to leave the asteroid field only after your navigation",
                       "determines a route back to Earth, which takes approximately 15 seconds",
                       "Quick Play:","Try and earn as much points as you can while dodging asteroids!",
                       "You get points from suriving and collecting asteroids. You get unlimited",
                       "collection range, but be careful: the longer you survive the more",
                       "difficult it gets. Asteroids will get faster, and the number",
                       "of them on screen will increase!"]

#the rect list for drawing the game selection menu
selectGameRectList = [Rect(240,150,240,300),Rect(520,150,240,300),Rect(530,100,160,40)] #list of rects for the buttons 
selectGameTextList = ["Story Mode","Quick Play","Leaderboards"]                         #list of the text for the button

#the array of rects for drawing the save selection menu
selectSaveButtonRect = [Rect(150,200,500,100),Rect(150,350,500,100),Rect(150,500,500,100),Rect(700,610,200,60),
                            Rect(700,200,200,100),Rect(700,350,200,100),Rect(700,500,200,100)]
selectSaveButtonText = ["Save 1","Save 2","Save 3","Delete a Save","Delete","Delete","Delete"]

#the arrays for the rects in the story main menu
storyHubMenuRect = [Rect(10,0,100,60),Rect(120,0,100,60),Rect(230,0,200,60),Rect(440,0,200,40),Rect(690,0,300,80),
                    Rect(230,60,200,30)]
storyHubMenuText = ["Quit","Save","Upgrades","Generate Energy","Launch","Base Upgrades"]

#the array of the rects for drawing the resource text
resourceCounters = [Rect(440,50,80,40),Rect(530,50,80,40),Rect(720,100,270,60)]
resourceType = ["Energy","Hydro","Power Progress"]        

#the array of rects for the base upgrades
upgradeBaseList = [Rect(100,250,300,50),Rect(100,320,300,50),Rect(100,390,300,50)]



#the list of text/rects for converting the fuel to energy - story mode
convertMenuText = ["+1","+5","+10","+25","Clear","Convert","amt","rslt"]
convertMenuRect = [Rect(100,400,50,50),Rect(160,400,50,50),Rect(220,400,50,50),Rect(280,400,60,50),Rect(350,400,80,50),
                   Rect(300,470,150,60),Rect(100,320,400,50),Rect(600,320,200,50)]
#the array of the text/rect for drawing the win screen
winGameMenuRect = [(500,150),(500,220),(500,250),(500,280),(500,310),(300,360),(500,400),(500,440),(500,480)]
winGameMenuText = ["Congratulations!","You sucessfully managed to generate enough power",
                   "to satisfy all of the computers on Earth.",
                   "Now that they are all online, your mission is completed.",
                   "You've done a great job",
                   "Statistics:","death","collected","energy"]
#the array of buttons for the win screen
winGameButtonRect = [Rect(200,510,250,60),Rect(550,510,250,60)]
winGameButtonText = ["Main Menu","Keep Playing"]

#the list of rects and text for the results of the expedition - story mode
resultsRectList = [(500,150),(500,195),(500,225),(500,295),(500,345),(500,390),(500,430)]       #the array of coordinates for text
resultsTextWinList = ["titleMessage","You get 100% of the fuel collected"," ","From your mission, you collected:","amt",
                      "The ship is getting refueled, and should be ready soon","eng"] #the text array for if the player survives
resultsTextLoseList = ["titleMessage","The ship's autonomous controller steered it back,","but you only get 25% of the fuel",
                       "From the damaged ship, we were able to collect:","amt",
                       "The ship should be repaired and ready to go soon","eng"]#the text array for if the player dies

#the array of rects and text for creating the name save file
getNameRectList = [Rect(150,100,700,100),Rect(250,400,500,60),Rect(450,500,160,50)]
getNameTextList = ["Enter a name for your save file","name","Confirm"]



deathInfo1 = renderText(fontMainMenu,"You Died!",WHITE)
deathInfo2 = renderText(fontButton,"You Scored:",WHITE)

deathNameRect = Rect(200,350,600,100)
deathButton1 = renderText(fontButton,"Check Rankings",WHITE)
deathButtonRect = getAlteredImage(deathButton1,(500,550),"center")

saveFileText = renderText(fontMainMenu,"Choose a Save File",WHITE)

leaderBoardText = renderText(fontButton,"Current Rankings",WHITE)

closeWindow = renderText(fontMainMenu," x ",WHITE)
closeWindowRect = getAlteredImage(closeWindow,(900,50),"center")

#loading all the images used
titleImage = image.load("assets/title.jpg")
eScreen = Rect(0,0,titleImage.get_width(),titleImage.get_height())
field1 = image.load("assets/field1.jpg")
mainModeImg = image.load("assets/mainModeImg.png")
quickPlayImg = image.load("assets/quickPlayImg.png")
dimScreen = image.load("assets/backgroundDim.png")

launchButton = Rect(670,30,300,60)

circleTemp = image.load("assets/circleArea.png").convert_alpha()
circleArea = ""
circleAreaRect = ""

storyModeOverlay = image.load("assets/storyOverlay.png").convert_alpha()

ship = image.load("assets/shipBody.png").convert_alpha() #assembles the ship list with the basic parts
shipPartList[0] = ship
shipL = image.load("assets/shipBodyLarge.png").convert_alpha()
shipPartListLarge[0] = shipL
buildShipParts()


mainThrust = image.load("assets/mainThrustsmall.png").convert_alpha()
thrustRect = Rect(417,327,45,45)

initFile = open("src/loadAssets.dat","r") #file that contains the path to all of the background images
imageQueue = initFile.readline().rstrip("\n").split(",") #read the line, and splits it by the comma
for img in imageQueue:                      #for loop to process all of the images
    asteroidTemp = image.load(img).convert_alpha()          #loading image
    astBackground.append(asteroidTemp)      #puts in into the list of background asteroids
    
for x in range(len(imageQueue)):            #for loop for creating the rect objects that go with the asteroid images
    if (x+3) % 4 == 0:
        rectTemp = Rect(0,(((x+3)/4)-1)*200,512,288)
    elif (x+2) % 4 == 0:
        rectTemp = Rect(500,(((x+2)/4)-1)*200,512,288)
    elif (x+1) % 4 == 0:
        rectTemp = Rect(1000,(((x+1)/4)-1)*200,512,288)
    else:
        rectTemp = Rect(-500,((x/4)-1)*200,512,288)
    astRectBack.append(rectTemp)
    
imageQueue = initFile.readline().rstrip("\n").split(",") #getting the list of images for normal surface asteroids

for img in imageQueue:
    asteroidTemp = image.load(img).convert_alpha()
    avalAstImage.append(asteroidTemp)
    
imageQueue = initFile.readline().split(",") #getting list of images for hydrogen/special collection asteroids

for img in imageQueue:
    asteroidTemp = image.load(img).convert_alpha()
    avalAstHydImage.append(asteroidTemp)
    
initFile.close()

asteroidTemp = image.load("assets/asteroidHydro1.png")
avalAstHydImage.append(asteroidTemp)
asteroidTemp = image.load("assets/asteroidHydro2.png")
avalAstHydImage.append(asteroidTemp)

buttnSrtBack = Rect(130,250,100,40) #the rect objects for the button labels
buttnHlpBack = Rect(130,350,100,40)
buttnQutBack = Rect(130,450,100,40)

loadUpgrades()                      #call the function to load the upgrade info
#restricts what events can be called to increase performace slightly
event.set_allowed([QUIT, KEYDOWN, KEYUP,MOUSEBUTTONDOWN,MOUSEBUTTONUP])

############################################## main code loop ##########################################################################

while True:
    #print("frame")
    mouseCoord = mouse.get_pos()#gets the mouse coordinates
    click = False
    for even in event.get(): #event handler
        #print(even)
        if even.type == QUIT: #if the command is quit, then exits and quits the program
            quit()
            exit() #prevents the pygame from giving more errors
            break #exits the while loop to prevent it from being run again
        elif even.type == MOUSEBUTTONDOWN:
            click = True
            mouseInfo = [even.pos,even.button]
        elif even.type == KEYDOWN:          #runs when the key is pressed down
            if needKey:
                keyPressed.append(even.unicode)
            if even.key in keyCode:         #checks if the key is on the list to prevent it from being called
                keyLoc = keyCode.index(even.key)    #looks for the index of the key
                keysActive[keyLoc] = 1              #changes it to true
        elif even.type == KEYUP:            #if the key is up
            if even.key in keyCode:         #checks if it is in the list
                keyLoc = keyCode.index(even.key)    #looks for the index of the key id
                keysActive[keyLoc] = 0              #sets it to false
            
            
            
            
############################################## Main Menu ###########################################################
    if gameState == 0: #main menu
        screen.blit(titleImage,eScreen)                 #drawing the background for main menu
        
        
        if subGameState == 0:   #Main Menu, if there is no window open
            
            draw.rect(screen,GREY,(130,75,450,100))
            screen.blit(mainMenuTitle,Rect(150,75,400,100)) #draws the title                  
            
            #drawing the ship parts for the main menu
            for x in range(5):
                screen.blit(shipPartListLarge[x+1],getAlteredImage(shipPartListLarge[x+1],(partLoc[x][0]+200,
                                                                                           partLoc[x][1]),"center"))
            #drawing the overall ship part (the frame)
            screen.blit(shipPartListLarge[0],getAlteredImage(shipPartListLarge[0],(700,350),"center"))
            
            
            #activ = ""
            #for x in keysActive:
                #activ += str(x)
            #testing = renderText(fontDev,activ,WHITE)       #drawing the inputs to make it easier to see potential problems
            #keysText = renderText(fontDev,"wsadqe",WHITE)
            #temp = renderText(fontDev,"keys currently pressed",WHITE)
            
            #shorterTest = renderText(fontDev,getShortenedPower(125),WHITE)
            #creen.blit(shorterTest,getAlteredImage(shorterTest,(900,600),"center"))
            #screen.blit(temp,Rect(850,660,10,10))
            #screen.blit(keysText,Rect(900,670,10,10))
            #screen.blit(testing,Rect(900,680,10,10))
            
            
            #drawing the buttons 
            if buttnSrtBack.collidepoint(mouseCoord):                        #detecting if mouse is hovering over button (start game)
                draw.rect(screen,GREY,buttnSrtBack.move(10,0).inflate(25,5))    #draws the enlarged version of the button
                screen.blit(buttonStartE,buttnSrtBack.move(5,0).inflate(0,5))   #draws the text for button
            else:                                                               #If the mouse is not hovering over button
                draw.rect(screen,GREY,buttnSrtBack.inflate(5,3))                #draws the button colour
                screen.blit(buttonStart,buttnSrtBack)                           #draws the normal sized button
                
            if buttnHlpBack.collidepoint(mouseCoord):
                draw.rect(screen,GREY,buttnHlpBack.move(10,0).inflate(25,5))
                screen.blit(buttonHelpE,buttnHlpBack.move(5,0).inflate(0,5))
            else:
                draw.rect(screen,GREY,buttnHlpBack.inflate(5,3))
                screen.blit(buttonHelp,buttnHlpBack)
            
            if buttnQutBack.collidepoint(mouseCoord):
                draw.rect(screen,GREY,buttnQutBack.move(10,0).inflate(25,5))
                screen.blit(buttonQuitE,buttnQutBack.move(5,0).inflate(0,5))
            else:
                draw.rect(screen,GREY,buttnQutBack.inflate(5,3))
                screen.blit(buttonQuit,buttnQutBack)
                
            if click == True:                                   #if the mouse if clicked
                click = False                                   #set the mouse to not be clicked
                if mouseInfo[1] == 1:                               #if the left mouse button was clicked
                    if buttnSrtBack.collidepoint(mouseInfo[0]):     #if the mouse clicked the start button
                        subGameState = 1                             #changes the game state, 1 is menu
                    elif buttnHlpBack.collidepoint(mouseInfo[0]):   #if the mouse clicked the help button
                        subGameState = 2                            #change the sub-state (will stay on menu, but have a panel drawn)
                    elif buttnQutBack.collidepoint(mouseInfo[0]):   #if the quit button was clicked
                        quit()          #quits pygame, then exits just to make sure nothing breaks
                        exit()
                        break
               
        

        elif subGameState == 1: #the menu for game select
            
            for x in range(len(selectGameRectList)):                                #goes through each rect obj on the list
                if selectGameTextList[x] == "Leaderboards":                         #if the text is leaderboards
                    tempText = renderText(fontInfo,selectGameTextList[x],WHITE)     #it renders the text with a different font
                else:
                    tempText = renderText(fontButton,selectGameTextList[x],WHITE)   #default text 
                    
                if selectGameRectList[x].collidepoint(mouseCoord):                  #detecting if the mouse is hovering over the button
                    draw.rect(screen,DARK_GREY,selectGameRectList[x])               #draws the button with a dark background
                    
                    if x != 2:                                                      #if the button index is not 2
                        draw.rect(screen,GREY,(200,475,650,100))                    #drawing the info panel that pops up
                        if selectGameTextList[x] == "Story Mode":                   #if the button is for story mode
                            #generates the two lines of description for story mode
                            infoText1 = renderText(fontInfo,"Embark on the quest to keep earth's computers powered",WHITE)
                            infoText2 = renderText(fontInfo,"with player progression and upgrades",WHITE)
                        else:                                                       #if the button is quick play
                            #generates the description for quick play
                            infoText1 = renderText(fontInfo,"Start a game immediately and compete with others to",WHITE)
                            infoText2 = renderText(fontInfo,"see how long you can last on the local leaderboard",WHITE)
                            
                        screen.blit(infoText1,(205,475,10,10))                      #blits the desciption onto the panel
                        screen.blit(infoText2,(205,510,10,10))
                        
                    if click:
                        click = False
                        if selectGameTextList[x] == "Story Mode":
                            gameState = 3                                               #change the game state to choosing the save file
                            subGameState = 0
                            
                            rebuildSaveFileArray()
                                    
                        elif selectGameTextList[x] == "Quick Play":
                            gameState = 1                   #changes game state to play asteroids
                            subGameState = 1                #uses the sub game state variable to tell program that it is quickplay
                            loadSaveFile("src/playerData/quickPlayStats.dat",1)
                            
                        elif selectGameTextList[x] == "Leaderboards":   #if the button label is leaderboards
                            gameState = 2                               #change state to leaderboards
                            subGameState = 0                            #set the substate to 0
                            loadLeaderboards()                          #load all of the leaderboards from the file
                            #the leaderboards load here instead of in the game state for it because it only needs to be loaded once
                else:
                    draw.rect(screen,GREY,selectGameRectList[x])        #if the button is not hovered over
                    
                if x == 0:                                      #if the rect is the first index, draw things for story mode
                    screen.blit(mainModeImg,getAlteredImage(mainModeImg,selectGameRectList[x].move(0,40).center,"center")) 
                    screen.blit(tempText,getAlteredImage(tempText,(360,200),"center"))
                elif x == 1:                                    #if the rect is for the second button, draw s
                    screen.blit(quickPlayImg,getAlteredImage(quickPlayImg,selectGameRectList[x].move(0,40).center,"center"))
                    screen.blit(tempText,getAlteredImage(tempText,(640,200),"center"))
                else:
                    screen.blit(tempText,getAlteredImage(tempText,selectGameRectList[x].center,"center"))
                    
                        
            if keysActive[6]: #if the esc key is pressed
                subGameState = 0    #goes back to the main menu            
                        
            
                
        elif subGameState >= 2: #the window that displays all the commands
            
            draw.rect(screen,GREY,(50,100,900,550))#drawing the window background
            
            if subGameState == 2:
                for x in range(len(helpScreenRectList1)):                    #drawing all of the text from the list
                    if helpScreenTextList1[x] == "How to Play":              #making the title a different font
                        tempText = renderText(fontMainMenu,helpScreenTextList1[x],WHITE)
                    elif (helpScreenTextList1[x] == "Objectives" or helpScreenTextList1[x] == "General Controls" or 
                    helpScreenTextList1[x] == "Collecting Special Asteroids"):   #detecting if the text is a header
                        tempText = renderText(fontButton,helpScreenTextList1[x],WHITE) #header text will have a bigger font
                    else:
                        tempText = renderText(fontInfo,helpScreenTextList1[x],WHITE)     #default info font for all the normal text
                        
                    screen.blit(tempText,getAlteredImage(tempText,helpScreenRectList1[x],"left")) #drawing the text onto the screen
                    
            elif subGameState == 3:
                for x in range(len(helpScreenRectList2)):
                    if helpScreenTextList2[x] == "How to Play cont.":
                        tempText = renderText(fontMainMenu,helpScreenTextList2[x],WHITE)
                    elif helpScreenTextList2[x] == "Story Mode: Lore" or helpScreenTextList2[x] == "Objective:":
                        tempText = renderText(fontButton,helpScreenTextList2[x],WHITE)                    
                    else:
                        tempText = renderText(fontInfo,helpScreenTextList2[x],WHITE)
            
                    screen.blit(tempText,getAlteredImage(tempText,helpScreenRectList2[x],"left")) 
                    
            elif subGameState == 4:
                for x in range(len(helpScreenRectList3)):
                    if helpScreenTextList3[x] == "How to Play...3":
                        tempText = renderText(fontMainMenu,helpScreenTextList3[x],WHITE)
                    elif helpScreenTextList3[x] == "Story Mode: Other Helpful Things:" or helpScreenTextList3[x] == "Quick Play:":
                        tempText = renderText(fontButton,helpScreenTextList3[x],WHITE)                    
                    else:
                        tempText = renderText(fontInfo,helpScreenTextList3[x],WHITE)
            
                    screen.blit(tempText,getAlteredImage(tempText,helpScreenRectList3[x],"left"))  
                    
            #the 2 buttons for navigating the help menu
            helpScreenPrevWindow = Rect(150,600,170,40)
            helpScreenPrevText = renderText(fontInfo,"Previous Page",WHITE)
            helpScreenNextWindow = Rect(700,600,150,40)     #making the button rect
            helpScreenNextText = renderText(fontInfo,"Next Page",WHITE)     #rendering the text for the button
            
            #this part decides which buttons are drawn for navigating the help menu
            if subGameState > 1 and subGameState < 4:#if the sub game state is between 2-4, enables the button to go the the next page

                if helpScreenNextWindow.collidepoint(mouseCoord):               #detecting if the mouse is hovering over the button
                    draw.rect(screen,DARK_GREY,helpScreenNextWindow)            #drawing the button highlighted 
                    if click:                                                   #if a click is detected
                        click = False
                        subGameState +=1                                        #increase the sub state by 1
                else:
                    draw.rect(screen,DARKLIGHT_GREY,helpScreenNextWindow)       #if it is not hovered over, then draw the normal background
                #blitting the text
                screen.blit(helpScreenNextText,getAlteredImage(helpScreenNextText,helpScreenNextWindow.center,"center")) 
                
            if subGameState > 2 and subGameState < 5:   #if the sub state is not on the first page
                if helpScreenPrevWindow.collidepoint(mouseCoord):               #detecting if the mouse is hovering over the button
                    draw.rect(screen,DARK_GREY,helpScreenPrevWindow)            #drawing the button background as dark
                    if click:                                                   #if it is clicked
                        click = False                                           #set the click to false so it doesn't trigger other things
                        subGameState -=1                                        #go down 1 sub state
                else:
                    draw.rect(screen,DARKLIGHT_GREY,helpScreenPrevWindow)       #drawing the normal button background
                    
                screen.blit(helpScreenPrevText,getAlteredImage(helpScreenPrevText,helpScreenPrevWindow.center,"center"))                
                        
            if keysActive[6]: #if the esc key is pressed
                subGameState = 0    #goes back to the main menu            
                
        
########################################### Game Execution #########################################################
                
    elif gameState == 1: #the main game
        
        screen.blit(field1,eScreen) #drawing the background screen
        
        
        if keysActive[2]: #if the A key is pressed
            pDir += pRotation     #the ship rotates counterclockwise at a rate of 0.5 degrees
            if pDir > 360:  #making sure that once the value reaches 360, it goes back to 0
                pDir -= 360
                
        elif keysActive[3]: #if the D key is pressed
            pDir -= pRotation     #the ship rotates clockwise at a rate of 0.5 degrees
            if pDir < 0:    #making sure that the angles don't go below 0
                pDir += 360
        
        
        for part in shipPartList:   #goes through all the parts of the ship
            rotShip,boundRect = rot_center(part,pDir,(462,312)) #500,350 , rotates the ship parts
            shipPartRotate.append(rotShip)#adds them to another list
            
        pHitboxFront = getPartLoc((515,350),(500,350),getAngleChange(pDir,180))
        pHitboxBack = getPartLoc((485,350),(500,350),pDir)
        
        
        if keysActive[:2].count(1) >= 1 or keysActive[4:].count(1) >= 1: #detects if there is any keys pressed, ignoring A and D
            if keysActive[0] == 1:                                          #detects if W was pressed
                pChangeX,pChangeY = splitForceComp(pDir,pThrustPower)       #gets the movements in the x and y change
                pVelX += pChangeX                                           #adds/removes the forces from the net velocity
                pVelY += pChangeY
                
                rotMainThrust,rotThrustRect = rot_center(mainThrust,pDir,(thrustRect.center))
                rotThrustRect.center = getPartLoc(thrustRect.center,boundRect.center,pDir)   
                pQueueList.append(rotMainThrust)
                pQueueList.append(rotThrustRect)
                
            if keysActive[1] == 1:                                      #if S is pressed
                pChangeX,pChangeY = splitForceComp(getAngleChange(pDir,180),pSidePower) #going backwards
                pVelX += pChangeX
                pVelY += pChangeY                
            if keysActive[4] == 1:                                      #if Q is pressed
                pChangeX,pChangeY = splitForceComp(getAngleChange(pDir,270),pSidePower) #strafe right
                pVelX += pChangeX
                pVelY += pChangeY                
            if keysActive[5] == 1:                                      #if E is pressed
                pChangeX,pChangeY = splitForceComp(getAngleChange(pDir,90),pSidePower) #strafe left
                pVelX += pChangeX
                pVelY += pChangeY               
            pVelX = pVelX/pBrake
            pVelY = pVelY/pBrake    #the variable for dividing allows for upgrading ship
        else:
            if abs(pVelX) <= 1:
                pVelX = 0
            else:
                pVelX = pVelX/pBrake #the velocity is divided if there are no control inputs. 
            if abs(pVelY) <= 1:
                pVelY = 0
            else:
                pVelY = pVelY/pBrake    #the variable for dividing allows for upgrading ship

                
        
        
        for x in range(len(astRectBack)):                       #handling the background asteroids
            astRectBack[x] = astRectBack[x].move(-pVelX,pVelY) #changing the location of the rectangle to match the player's movement
            needChangeX,needChangeY = detectOffScreen(astRectBack[x],0) #sending the coordinates to check if it is off the screen
            if needChangeX != 0 or needChangeY != 0: #if it is, then shifts the coordinates to be on the opposite side of the screen
                astRectBack[x] = astRectBack[x].move(-(needChangeX*2000),-(needChangeY*900)) #if the other does not need a change, then it will
            #still be 0, because nothing is being added, only multiplied
            screen.blit(astBackground[x],astRectBack[x])        #drawing the background.
        
            
            
        #this for loop handles updating the coords of the asteroids    
        for x in range(len(astListRect)): #lists are astListRect,astListImg,astListVel,astListSize,astListType
            vectorMove = astListVel[x]                      #gets the x and y velocities from the list
            astListRect[x] = astListRect[x].move(-pVelX-vectorMove[0],pVelY-vectorMove[1]) #adds the player's x and y vel w/ the vectorMove
            isOffScreen = detectOffScreen(astListRect[x],300)#checks if the asteroid is off the screen, past boundaries (300px)
            noDraw = detectOffScreen(astListRect[x],0)
            
            if not noDraw[0] and not noDraw[1]:
                screen.blit(astListImg[x],astListRect[x])       #draws the asteroid if it is on the screen       
                
            if isOffScreen[0] != 0 or isOffScreen[1] != 0: #if the asteroid is off the screen
                astToBeRemoved.append(x)                    #adds the index of the asteroid to a queue
                #print("Queue: removing asteroid")
                
            if checkCircleCollision(pHitboxFront,astListRect[x].center,15,astListSize[x]) or checkCircleCollision( #checks if the player is
                pHitboxBack,astListRect[x].center,15,astListSize[x]):       #hit by an asteroid by getting distance between the 2 circles
                #print("death")
                
                if subGameState == 1: #if the player is playing the quick play mode
                    gameState = 2
                    loadLeaderboards()
                    needKey = True
                    
                else:
                    pStatus = False
                    gameState = 5 #sends the player back to the menu currently
                    pStoredFuel += int(pCurrentCapacity/4)
                    pCollectedTotal += int(pCurrentCapacity/4)
                    
                    pDeaths += 1
                    
                
            if click: #checking if the player has clicked the hydrogen asteroids
                if astListType[x]:       #checking if the player has clicked
                    if mouseInfo[1] == 1:#checking if the left mouse button was clicked
                        if checkCircleCollision(astListRect[x].center,mouseInfo[0],astListSize[x],5): #detecting if it is on the asteroid
                            if subGameState == 0:
                                if checkCircleCollision(astListRect[x].center,(500,350),astListSize[x],pRange) and pCurrentCapacity < pCapacity:
                                    #this is detecting if the player's ship is in range of the asteroid
                                    astToBeRemoved.append(x) #sends it to the remove queue
                                    pCurrentCapacity += astListSize[x]/10 #
                            else:
                                astToBeRemoved.append(x) #sends it to the remove queue
                                pCollectNum += 1#increases number of asteroids clicked
                                pPointsTotal += pPointCollectQuick #adds points, if it is the right mode
                            
            
            
        for x in range(len(astToBeRemoved)-1,-1,-1): #handles removing the asteroid from the lists
            removeAstFromList(astToBeRemoved[x],0)     #calls a function that will remove the entry from all arrays
            astToBeRemoved.pop(x)                       #removes the index from the list
            
            
        if len(astListRect) < difficultySetting:                #checks if there are enough asteroids on the screen
            for x in range(difficultySetting -len(astListRect)):#if there aren't, create enough until it meets the requirement
                genAst()                                        #calls the asteroid creating function

        
        for x in range(int(len(pQueueList)/2)): #handles the list of images attached to the ship
            forceRect = pQueueList.pop()        #the rectangle object is the second part of the image, so it gets popped first
            forceImage = pQueueList.pop()       #the image is the first most object that will be popped second
            screen.blit(forceImage,forceRect) #draws the image

        for x in range(len(shipPartRotate)-1,-1,-1):#goes through each rotated image on the array, starting at the last one
            screen.blit(shipPartRotate[x],boundRect) #draws it using the one rect object, they all have the same image size
            shipPartRotate.pop() #removes the ship image from the list
        
        if subGameState == 0:                                                   #drawing images/buttons when the player is doing story mode
            draw.rect(screen,BLUE,(15,15,pCurrentCapacity*(300/pCapacity),50))  #drawing the current amount of hydrogen the player has
                                                                #the 300/pCapacity makes sure that it will be 300px wide at max capacity
                                                                
            for x in range(int(pCurrentCapacity)+1):                                           #drawing the lines to separate each ton of fuel
                draw.line(screen,BLACK,(15+x*(300/pCapacity),15),(15+x*(300/pCapacity),65),1)   #the y values stay the same, x is dependent
                #on the current capacity.
            screen.blit(circleArea,circleAreaRect)  #drawing a visual area where asteroids can be collected

            screen.blit(storyModeOverlay,eScreen)
            if gameTimer < time.get_ticks():                        #detecting if 30 seconds have passed (30000 ticks = 30 sec)
                draw.rect(screen,MUTED_YELLOW,launchButton)                                         #drawing the active button
                launchText = renderText(fontButton,"Return to Base",DARK_GREY)                      #rendering the text for the button
                screen.blit(launchText,getAlteredImage(launchText,launchButton.center,"center"))    #blitting the text
                if launchButton.collidepoint(mouseCoord):                                           #detecting if the mouse is over it
                    if click:                                       #it is more efficient to check if the mouse is hovering over first
                        click = False                               #because every time the mouse clicks, it has to check collisions
                        gameState = 5                            #changing the game state to 5, the results screen
                        removeAstFromList(0,1)
                        pStoredFuel += int(pCurrentCapacity)
                        pCollectedTotal += int(pCurrentCapacity)
                        
            else:                                                   #if the 30 seconds have not passed
                draw.rect(screen,DARKLIGHT_GREY,launchButton)                           #draw the button as muted grey
                launchText = renderText(fontButton,"Calculating...",LIGHT_GREY)         #render text to show button is not active yet
                screen.blit(launchText,getAlteredImage(launchText,launchButton.center,"center"))  #blitting the image
                if launchButton.collidepoint(mouseCoord):                               #if the mouse is hovering over it
                    infoPanel = Rect(600,100,380,50)                                    #creating an info rect for the player
                    draw.rect(screen,GREY,infoPanel)                                    #drawing the panel
                    infoText = renderText(fontInfo,"Return route being calculated",WHITE)       #rendering info text
                    screen.blit(infoText,getAlteredImage(infoText,infoPanel.center,"center"))   #blitting text on the center of the rect
                
        
        if subGameState == 1:                               #runs only when the player is in quick play mode
            if pTimeSincePoints + 5000 <= time.get_ticks(): #if 5 seconds have passed
                pTimeSincePoints = time.get_ticks()         #makes the timer equal to the new time
                pPointsTotal += pPointGameQuick             #adding the points
                difficultySetting += 1                      #adds another asteroid that is able to be spawned
                astSpeedMult += 0.1
            
            currentPoints = renderText(fontButton,str(pPointsTotal),WHITE) 
            screen.blit(currentPoints,getAlteredImage(currentPoints,(900,50),"right"))
                
        #detecting if the game is not being played anymore
        if gameState == 2 or gameState == 5:
            removeAstFromList(0,1)
            
        #drawing the hitboxes for testing purposes
        #draw.circle(screen,BLUE,(int(pHitboxFront[0]),int(pHitboxFront[1])),15)
        #draw.circle(screen,BLUE,(int(pHitboxBack[0]),int(pHitboxBack[1])),15)
        ### dev text for seeing variables
        #thrustXText = renderText(fontDev,"Thrust X-axis: "+str(pChangeX)+" Net: "+str(pVelX),WHITE)
        #thrustYText = renderText(fontDev,"Thrust Y-axis: "+str(pChangeY)+" Net: "+str(pVelY),WHITE)
        #deg = renderText(fontDev,"Current ship Orientation: "+str(pDir),WHITE)
        fpsCurrent = int(fpsClock.get_fps())
        fpsText = renderText(fontDev,"FPS: "+str(fpsCurrent),WHITE)
        screen.blit(fpsText,(950,10,50,50))
        #screen.blit(thrustXText,Rect(700,490,10,10))
        #screen.blit(thrustYText,Rect(700,500,10,10))
        #screen.blit(deg,Rect(800,480,10,10))        
       
       
       
################################################# Leaderboards ######################################################## 
        
        
    if gameState == 2: 
        #drawing the leaderboards window
        screen.blit(titleImage,eScreen)         #placing the background
        if subGameState == 0:                   #the main window that displays the leaderboards
            draw.rect(screen,GREY,(325,100,350,500))    #drawing the background for the leaderboard
            screen.blit(leaderBoardText,getAlteredImage(leaderBoardText,(500,150),"center"))
            for x in range(10):                         #rendering and drawing leaderboard positions
                if pIndex == x:
                    tempTextName = renderText(fontInfo,leaderBoards[x][0],YELLOW) #getting the name from the list
                    tempTextPoints = renderText(fontInfo,str(leaderBoards[x][1]),YELLOW)#getting the points of the name
                else: 
                    tempTextName = renderText(fontInfo,leaderBoards[x][0],WHITE) #getting the name from the list
                    tempTextPoints = renderText(fontInfo,str(leaderBoards[x][1]),WHITE)#getting the points of the name  
                
                screen.blit(tempTextName,(350,200+30*x,100,30))#drawing name
                screen.blit(tempTextPoints,getAlteredImage(tempTextPoints,(650,200+30*x),"right"))#drawing the number of points
                
            draw.rect(screen,GREY,closeWindowRect.inflate(4,4)) #draws the button to close the screen
            screen.blit(closeWindow,closeWindowRect) #drawing the text for the button
            
            if keysActive[6]: #if the user hits esc
                gameState = 0
                pIndex = 11
            elif click:
                if closeWindowRect.collidepoint(mouseCoord):
                    gameState = 0
                    pIndex = 11
                
        elif subGameState == 1: #drawing the player death screen
            
            for x in range(len(keyPressed)-1,-1,-1): #handling the text input from player
                if keyPressed[x] == '\x08': #if the backspace key is pressed
                    if len(textBox) > 0:        #if there more than 0 characters in the string to prevent crashing
                        textBox = textBox[:-1]  #removes the last letter
                elif keyPressed[x] == '~':      #prevents the user from having the ~ in their name to prevent the file errors
                    none = False                #meaningless variable
                elif keyPressed[x] == ',':      #prevents the user from having a comma in their name to prevent errors
                    none = False                #meaningless variable
                elif len(textBox) >= 16:        #preventing the user from having a very long name
                    none = False
                elif keyPressed[x] == '\r':
                    if len(textBox) > 0:
                        needKey = False
                        subGameState = 0            
                        pIndex = updateLeaderboards(pPointsTotal,textBox)
                        resetPlayerStats()                    
                else:
                    textBox += keyPressed[x]    #if nothing preventing user from inputting the current key, add to string.
                keyPressed.pop()                #removes the current key
                
            name = renderText(fontButton,textBox,BLACK)     #renders the current text
            draw.rect(screen,GREY,(150,100,700,300))        #draws the background
            finalScore = renderText(fontButtonSelect,str(pPointsTotal),YELLOW)      #rendering the score that user got
            
            screen.blit(deathInfo1,getAlteredImage(deathInfo1,(500,150),"center"))  #blitting the death text
            screen.blit(deathInfo2,getAlteredImage(deathInfo2,(500,250),"center"))  #the text is rendered before the main loop
            screen.blit(finalScore,getAlteredImage(finalScore,(500,300),"center"))  
            draw.rect(screen,WHITE,deathNameRect)                                   #drawing the white text box
            screen.blit(name,deathNameRect.move(10,10))
            draw.rect(screen,GREY,deathButtonRect.inflate(5,5))
            screen.blit(deathButton1,deathButtonRect)                               #drawing the button that user clicks
            if click:
                if deathButtonRect.collidepoint(mouseCoord) and len(textBox) > 0:
                    needKey = False
                    subGameState = 0            
                    pIndex = updateLeaderboards(pPointsTotal,textBox)
                    resetPlayerStats()
            
    #################################### Save Files ########################################################
    
    elif gameState == 3:
        screen.blit(titleImage,eScreen)                 #drawing the background
        screen.blit(saveFileText,getAlteredImage(saveFileText,(500,100),"center")) #drawing the title for the screen
        
        for x in range(len(selectSaveButtonRect)):                              #for loop that goes through all of the rects in the list
            
            if x <= 2:      #this runs for the first 3 indexes
                tempText = renderText(fontButton,selectSaveButtonText[x],WHITE) #generates the save file number text
                
                if isSaveEmptyList[x]:                                      #before rendering the name of the save it detects if it is empty
                    saveName = renderText(fontButtonSelect,saveNameList[x],LIGHTRED)    #renders the name with a red tone
                else:
                    saveName = renderText(fontButtonSelect,saveNameList[x],WHITE)  
                    
                if selectSaveButtonRect[x].collidepoint(mouseCoord):                        #detecting if mouse is hovering over button
                    draw.rect(screen,DARK_GREY,selectSaveButtonRect[x])
                    if click:                                                               #detecting if there was a click
                        click = False
                        #print("save clicked")
                        if isSaveEmptyList[x]:                                  #true means that the save is empty
                            loadSaveFile("src/playerData/saveDefault.dat",1)    #loads the default save file containing the starting stats                  
                            gameState = 6                                       #sets the game state to getting the name of the save file
                            saveFileIndex = saveFileList[x]                     #setting which file to be used
                            needKey = True                                      #sets the key logging to true
                            buildShipParts()                                    #calls function to rebuild ship parts
                            #print("not empty")
                        else:
                            gameState = 4                                       #sets the game state to the story hub menu
                            saveFileIndex = saveFileList[x]
                            loadSaveFile(saveFileIndex,1)                       #loads the full save file
                            buildShipParts()                                    #calls the function to add correct parts to the array
                else:
                    draw.rect(screen,GREY,selectSaveButtonRect[x])              #drawing the button background normally
                    
                screen.blit(tempText,getAlteredImage(tempText,(175,210+150*x),"left"))  #blits the save spot
                screen.blit(saveName,getAlteredImage(saveName,(250,250+150*x),"left")) 
                
            if x == 3:                                                          #if the index is for button to delete save file
                tempText = renderText(fontInfo,selectSaveButtonText[x],WHITE)   #renders the text
                if selectSaveButtonRect[x].collidepoint(mouseCoord):            #detecting if the mouse is hovering over it
                    draw.rect(screen,DARK_GREY,selectSaveButtonRect[x])         #drawing the darker button background
                    if click:                                                   #if the click is detected
                        click = False                                           #setting the click to false
                        isDeleteSaveFile = True                                 #enables variable to show delete buttons
                else:
                    draw.rect(screen,GREY,selectSaveButtonRect[x])              #drawing the button background normally
                    
                screen.blit(tempText,getAlteredImage(tempText,selectSaveButtonRect[x].center,"center")) #blits the text in the center
                
            if isDeleteSaveFile and x >= 4:                                     #detects if the delete save file is true, 
                                                                                #and is correct index
                tempText = renderText(fontInfo,selectSaveButtonText[x],WHITE)   #rendering the text
                
                if selectSaveButtonRect[x].collidepoint(mouseCoord):            #detecting if the mouse is in the rect
                    draw.rect(screen,DARK_RED,selectSaveButtonRect[x])               #drawing the button darker shade of red
                    if click:                                                   #if a click was detected
                        click = False                                           #setting click to false
                        isDeleteSaveFile = False                                #setting the delete save file to false
                        deleteSaveFile(saveFileList[x-4])                       #calls the function to reset save file with specific index
                        
                        rebuildSaveFileArray()                                  #calls the function to rebuild the array of save files
                else:                                                           #if the button is not selected
                    draw.rect(screen,RED,selectSaveButtonRect[x])               #draw in normal red
                    
                screen.blit(tempText,getAlteredImage(tempText,selectSaveButtonRect[x].center,"center"))   #blitting the text to screen             
            
                
  #blits the save name
            
            
############################################# Main Screen for Story Mode ##########################################################
                        
    elif gameState == 4:
        screen.blit(titleImage,eScreen)                 #drawing the background        
        
        if subGameState == 0:           #main (hub) menu for story mode
            
            for x in range(5):          #runs 5 times
                screen.blit(shipPartListLarge[x+1],getAlteredImage(shipPartListLarge[x+1],partLoc[x],"center"))  
                #drawing the current ship parts from the list
            screen.blit(shipPartListLarge[0],getAlteredImage(shipPartListLarge[0],(500,350),"center"))
            
                                        
        elif subGameState == 1:         #upgrading menu
            
            highlightObjectIndex = 10   #sets the highlighted part to an impossible number
            
            for x in range(len(upgradeLabelRectList)):                      #goes through each label for each part
                
                tempText = renderText(fontInfo,upgradeNameList[x],WHITE)    #renders the text that contains the name of the part
                tempRect = getAlteredImage(tempText,upgradeLabelRectList[x],"center")  #gets the rect
                if shipPartUpgradedList[x] == 0:
                    draw.rect(screen,GREY,tempRect.inflate(10,10))              #draws the background for the label
                else:
                    draw.rect(screen,DARK_GREY,tempRect.inflate(10,10))              #draws the background for the label
                    
                screen.blit(tempText,tempRect)                              #blitting the name
                
                if tempRect.collidepoint(mouseCoord):                       #detecting if the mouse is hovering over the label
                    highlightObjectIndex = x                                #setting the index to the label's index
                    draw.rect(screen,GREY,(30,590,930,80))                  #drawing the background for description and info
                    descPart = renderText(fontInfo,upgradeDescList[x],WHITE)    #rendering text for description
                    effectPart = renderText(fontInfo,upgradeEffectList[x],WHITE)#rendering text for effect of upgraded part
                    costPart = renderText(fontInfo,"Cost: "+getShortenedPower(upgradeCostList[x]),WHITE)  #rendering the cost of the part
                    
                    screen.blit(descPart,getAlteredImage(descPart,(50,600),"left"))         #Blitting text to the description
                    screen.blit(effectPart,getAlteredImage(effectPart,(50,630),"left"))
                    screen.blit(costPart,getAlteredImage(costPart,(950,630),"right"))
                    
                    if click:                                       #if the button was clicked, then try upgrade
                        click = False                               #setting the click to false
                        if pStoredEnergy < upgradeCostList[x]:      #testing to see if player can afford upgrade
                            gameTimer = time.get_ticks()+2000       #if they can't, then launch timer to inform
                        else:                                       #if player can afford part
                            if shipPartUpgradedList[x] == 0:        #testing to see if it is already upgraded
                                
                                shipPartUpgradedList[x] = 1         #make the part upgraded in the array
                                pStoredEnergy -= upgradeCostList[x] #removes the amount that the part cost from the player's storage
                                upgradeStat(x)                                
                                buildShipParts()                    #calls the function to rebuild ship
                    
                    
            
            for x in range(5):                  #runs 5 times, goes through all parts
                if highlightObjectIndex == x:   #detecting if the highlighted part is the current part
                    screen.blit(shipPartListSelect[x],getAlteredImage(shipPartListSelect[x],partLoc[x],"center")) #getting images from the
                    #highlighted images array instead of the normal large ship parts
                else:
                    screen.blit(shipPartListLarge[x+1],getAlteredImage(shipPartListLarge[x+1],partLoc[x],"center"))
            
            screen.blit(shipPartListLarge[0],getAlteredImage(shipPartListLarge[0],(500,350),"center"))
            
        
        elif subGameState == 2:         #menu for base upgrades
            draw.rect(screen,DARK_GREY,(50,100,900,550)) #drawing the background
            

            for x in range(len(upgradeBaseList)):                                   #going through all of the buttons to draw
                tempText = renderText(fontInfo,upgradeNameList[x+5],WHITE)          #rendering the name of the upgrade
                techLevel = renderText(fontInfo,"lvl."+str(baseUpgraded[x]),WHITE)  #getting the level of the text, adding lvl to the str
                techCost = int(upgradeCostList[x+5]+(upgradeCostList[x+5]*0.25*baseUpgraded[x]))
                costPart = renderText(fontInfo,"Cost: "+getShortenedPower(techCost),WHITE)  #getting the cost of the upgrade
                
                
                #the index for the upgrade name/other info is x+5 because the first 5 are ship upgrades
                
                if upgradeBaseList[x].collidepoint(mouseCoord):                     #detecting if the mouse is hovering over it
                    draw.rect(screen,DARKLIGHT_GREY,upgradeBaseList[x])             #drawing the background of the button darker
                    draw.rect(screen,GREY,(100,470,800,130))                        #drawing the description window
                    descPart = renderText(fontInfo,upgradeDescList[x+5],WHITE)      #getting the description of the upgrade
                    #costPart = renderText(fontInfo,"Cost: "+getShortenedPower(upgradeCostList[x+5]),WHITE)  #getting the cost of the upgrade
                    #the function get shortened power automatically gets the right factor, eg. 1000 MW = 1.0GW, and returns that
                    effectPart = renderText(fontInfo,upgradeEffectList[x+5],WHITE)  #gets the upgrade effect desc and rendering it
                    
                    screen.blit(descPart,(110,495,100,50))                          #placing the desciption
                    screen.blit(effectPart,(110,540,100,50))                        #placing the upgrade effect
                    
                    if click:                                       #detecting if the player has clicked
                        click = False                               #setting it to false
                        if pStoredEnergy < techCost:      #testing to see if player can afford upgrade
                            gameTimer = time.get_ticks()+2000       #if they can't, then launch timer to inform
                        else:
                            baseUpgraded[x] += 1                  #upgrade the base tech by 1 level, there is no need to change stat,
                            #the change is determined/added in the actual calculation, unlike ship parts
                            pStoredEnergy -= techCost #removes the amount that the part cost from the player's storage
                    
                else:
                    draw.rect(screen,GREY,upgradeBaseList[x])       #draw the normal button if not selected
                
                
                screen.blit(techLevel,getAlteredImage(techLevel,upgradeBaseList[x].move(200,0).center,"center"))    #blitting the name
                screen.blit(tempText,getAlteredImage(tempText,upgradeBaseList[x].center,"center"))                  #blitting the level
                screen.blit(costPart,getAlteredImage(costPart,upgradeBaseList[x].move(500,0).center,"right_center"))#placing the cost of upgrade, right justified
                
                
            
            
            
        elif subGameState == 3: #converting resources menu
            draw.rect(screen,DARK_GREY,(50,100,900,500)) #drawing the background
            
            for x in range(len(convertMenuRect)):   #going through all of the rect objects for the converting menu
                if convertMenuText[x] == "amt":      #if the text is the same, then get the converting amount as the text
                    tempText = renderText(fontButton,str(pConvertAmount)+" tons",WHITE) #typecasts the variable to get the text
                    tempRect = getAlteredImage(tempText,convertMenuRect[x].topleft,"left")  #positions it to the left on the rect
                elif convertMenuText[x] == "rslt":                #if the text is the same, then get the potential end result of convert
                    tempText = renderText(fontButton,getShortenedPower(pConvertAmount*(50+baseUpgraded[0]*25)),WHITE) #gets the energy 
                    #that would be converted, with the upgrades accounted for
                    tempRect = getAlteredImage(tempText,convertMenuRect[x].center,"center") #gets the rect for the image in the center                   
                else:                                                                        #the default text
                    tempText = renderText(fontInfo,convertMenuText[x],WHITE)                
                    tempRect = getAlteredImage(tempText,convertMenuRect[x].center,"center")
                    
                draw.rect(screen,GREY,convertMenuRect[x])   #drawing the button background
                screen.blit(tempText,tempRect)              #blitting the text onto the button
                
                if convertMenuRect[x].collidepoint(mouseCoord):     #detecting if the mouse is hovering over the button
                    if click:                                       #if the mouse has clicked
                        click = False                               #set the boolean to false
                        if convertMenuText[x] == "+1":              #depending on the text, add a specific amount to how much is converted
                            pConvertAmount += 1                     #adds 1 ton to the convert variable
                        elif convertMenuText[x] == "+5":
                            pConvertAmount += 5
                        elif convertMenuText[x] == "+10":
                            pConvertAmount += 10
                        elif convertMenuText[x] == "+25":
                            pConvertAmount += 25
                        elif convertMenuText[x] == "Clear":         #if the button was the clearing one
                            pConvertAmount = 0                      #reset the amount to convert to 0
                        
                        if pConvertAmount > pStoredFuel:            #checks if the amount to convert is below the amount the player has
                            pConvertAmount = pStoredFuel            #if it is higher, then set the amount to the amount player has
                            
                        if convertMenuText[x] == "Convert":         #if the button clicked was convert
                            pStoredFuel -= pConvertAmount           #removes the fuel amount from the player
                            pStoredEnergy += pConvertAmount*(50+baseUpgraded[0]*25)   #adds the amount of energy to the energy storage
                            pEnergyTotal += pConvertAmount*(50+baseUpgraded[0]*25)
                            print(str(pConvertAmount*(50+baseUpgraded[0]*25)))
                            pConvertAmount = 0                      #sets the amount to convert to 0
                            
                
            generateInstruct = renderText(fontButton,"Use Your Hydrogen Fuel to Generate Energy",WHITE)
            generateInstruct2 = renderText(fontInfo,"With the current technology, you can generate ",WHITE)
            generateInstruct3 = renderText(fontInfo, getShortenedPower(50+ baseUpgraded[0]*25)+
                                           " of power from 1 ton of hydrogen",WHITE)
            generateInstruct4 = renderText(fontInfo,"Use the energy to power Earth's computers, so they can upgrade your tech",WHITE)
            screen.blit(generateInstruct,(100,150,100,100))
            screen.blit(generateInstruct2,(100,200,100,100))
            screen.blit(generateInstruct3,(100,225,100,100))
            screen.blit(generateInstruct4,(100,250,100,100))
            
            
        
        if subGameState == 6:       #subState for menu telling players they've won
            draw.rect(screen,GREY,(50,100,900,500)) #drawing the background
        
            for x in range(len(winGameMenuRect)):   #going through all of the coords in the list
                if winGameMenuText[x] == "death":       #if the text calls for the player deaths, make the text show the number of deaths
                    tempText = renderText(fontInfo,"You have crashed "+str(pDeaths)+" times.",WHITE)
                elif winGameMenuText[x] == "collected":                             #this calls for the players collected fuel total stat
                    tempText = renderText(fontInfo,"You collected "+str(pCollectedTotal)+" tons of hydrogen.",WHITE)
                elif winGameMenuText[x] == "energy":                                #this calls for the player's total energy generated stat
                    tempText = renderText(fontInfo,"You generated "+getShortenedPower(pEnergyTotal)+" for personal upgrades.",WHITE)
                elif winGameMenuText[x] == "Congratulations!":                      #if the text is congrats, then make it bigger
                    tempText = renderText(fontButtonSelect,winGameMenuText[x],WHITE)
                else:#
                    tempText = renderText(fontInfo,winGameMenuText[x],WHITE)        #rendering the text in the default font
                    
                 #blits the text onto the screen centered on the coordinated from the list
                screen.blit(tempText,getAlteredImage(tempText,winGameMenuRect[x],"center"))
            
            for x in range(len(winGameButtonRect)):                             #the for loop handles the buttons for the win menu
                tempText = renderText(fontButton,winGameButtonText[x],WHITE)    #rendering the text, there is no special cases for this
                if winGameButtonRect[x].collidepoint(mouseCoord):               #detecting if it hovered over
                    draw.rect(screen,DARK_GREY,winGameButtonRect[x])            #drawing the background in a dark tone
                    
                    if click:                                                   #if a click was detected
                        click = False
                        if winGameButtonText[x] == "Main Menu":                 #if the button label was main menu
                            subGameState = 0                                     #setting subgamestate to 0 to prevent issues
                            gameState = 0                                       #setting the game state to 0 
                            updateSaveFile(saveFileIndex)                       #saving the game automatically
                        else:                                           #if the other button is pressed, 
                            subGameState = 0                                    #sends the player to the story hub menu (substate 0)
                else:
                    draw.rect(screen,DARKLIGHT_GREY,winGameButtonRect[x])       #draws the button in a lighter than dark grey, because
                    #the background for the win screen in already grey
                screen.blit(tempText,getAlteredImage(tempText,winGameButtonRect[x].center,"center"))    #blitting the text
           
                
        if not isAcceptedWin and (baseUpgraded[1]*125+baseUpgraded[2]*2000) >= 5000:    #detecting if the win screen is not shown and 
                                                                                        #has achieved the objective
            isAcceptedWin = True                                                        #changes variable to show that the screen is shown
            subGameState = 6                                                            #setting the substate to 6
            
            
        #for loop that is in charge of drawing all of the buttons for naviagtin of menus (subgamestate)
        for x in range(len(storyHubMenuRect)): #handling all of the buttons in the list
            
            if storyHubMenuText[x] == "Launch":             #changing the button font if the label is launch
                tempText = renderText(fontMainMenu,storyHubMenuText[x],WHITE)
            elif storyHubMenuText[x] == "Generate Energy" or storyHubMenuText[x] == "Base Upgrades":
                tempText = renderText(fontInfo,storyHubMenuText[x],WHITE)                    
            else:                                           #if there are no matches, the default text is rendered
                tempText = renderText(fontButton,storyHubMenuText[x],WHITE)
                
            doesBackwards = False #makes the variable initially false, so all the menus go to their destination
            
            if subGameState == 1 and storyHubMenuText[x] == "Upgrades": #if the subState is already on upgrades, then make it go to main menu
                doesBackwards = True
            elif subGameState == 2 and storyHubMenuText[x] == "Base Upgrades":
                doesBackwards = True
            elif subGameState == 3 and storyHubMenuText[x] == "Generate Energy": #if the substate is already on the generate, it will trigger
                doesBackwards = True
            
            if storyHubMenuRect[x].collidepoint(mouseCoord): #detecting if the mouse is hovered over the button
                draw.rect(screen,DARK_GREY,storyHubMenuRect[x]) #draws the button background with a darker tone
                if click:                                       #detecting if the mouse was clicked
                    click = False                               #setting the mouse clicked to false
                    if storyHubMenuText[x] == "Upgrades":       #if the mouse clicks the button that is labelled upgrades
                        if doesBackwards:
                            subGameState = 0                        #changes the state.
                        else:
                            subGameState = 1
                    elif storyHubMenuText[x] == "Base Upgrades":    #if the button that was clicked has name upgrades
                        if doesBackwards:                           #checks if it is already on that screen
                            subGameState = 0                        #sends player back to menu
                        else:
                            subGameState = 2
                    elif storyHubMenuText[x] == "Generate Energy":
                        if doesBackwards:
                            subGameState = 0
                        else:
                            subGameState = 3                        
                    elif storyHubMenuText[x] == "Quit":         #if the button labelled quit was clicked
                        gameState = 0                           #sends the player back to the main menu
                        subGameState = 0                        #changes the substate to 0 to prevent the wrong menu from being openned
                    elif storyHubMenuText[x] == "Save":         #if the save button is hit
                        updateSaveFile(saveFileIndex)           #calls function to overwrite save file
                        subGameState = 5                        #sets the sub game state to 5 (tells user game is saving)
                        gameTimer = time.get_ticks() + 500      #starts the brief timer
                    elif storyHubMenuText[x] == "Launch":       #if the launch button is clicked
                        subGameState = 0                        #set the sub-state to 0
                        gameState = 1                           #setting the game state to the main game
                        pStatus = True                          #resets the status of the player to alive
                        gameTimer = time.get_ticks() + 15000    #starts the game timer for 30 seconds (30000 ticks)
                        
                        
            elif doesBackwards:                                 #detecting if the button's menu is open
                draw.rect(screen,DARK_GREY,storyHubMenuRect[x]) #drawing the background as selected
            else:
                draw.rect(screen,GREY,storyHubMenuRect[x])      #if the mouse is not hovering over the button, do a normal background
                
            screen.blit(tempText,getAlteredImage(tempText,storyHubMenuRect[x].center,"center"))     #blits the text onto the button
            
        
        

        
        for x in range(len(resourceCounters)):  #goes through each of the rect objects
            draw.rect(screen,GREY,resourceCounters[x])  #draws the background based off the Rect
            
            if resourceType[x] == "Energy":             #detects which data to show, if the type is energy
                tempText = renderText(fontInfo,getShortenedPower(pStoredEnergy),YELLOW) #generates the text based off of the player data
            elif resourceType[x] == "Power Progress":
                tempText = renderText(fontInfo,getShortenedPower(baseUpgraded[1]*125000+baseUpgraded[2]*2000000)+"/5.0TW",BLACK)
                draw.rect(screen,YELLOW,(725,105,min((baseUpgraded[1]*125+baseUpgraded[2]*2000)/20,250),50))
            else:                                       
                tempText = renderText(fontInfo,str(pStoredFuel)+"t",BLUE) #generates the text from the fuel statistic, with the unit after
            screen.blit(tempText,getAlteredImage(tempText,resourceCounters[x].center,"center")) #blits the text in the center of rect
            
            if resourceCounters[x].collidepoint(mouseCoord):                                    #Detecting if the mouse is hovering over
                if resourceType[x] == "Power Progress":
                    tempDesc = renderText(fontInfo,"The power that all of Earth's computers require",WHITE)
                    draw.rect(screen,GREY,(450,170,545,40))
                    screen.blit(tempDesc,getAlteredImage(tempDesc,(722,190),"center"))
                else:
                    
                    draw.rect(screen,LIGHT_GREY,resourceCounters[x].move(0,50).inflate(170,0))      #draws the info popup panel                    
                    if resourceType[x] == "Energy":                                         #detecting which info to display by text
                        tempDesc = renderText(fontInfo,"Your Stored Energy",WHITE)          #energy info
                    else:
                        tempDesc = renderText(fontInfo,"Your Stored Hydrogen",WHITE)        #fuel info    
                    
                    screen.blit(tempDesc,getAlteredImage(tempDesc,resourceCounters[x].move(0,50).center,"center")) #blits it by the new rect
                    

                    
                #move position. It moves the normal rect, then gets the center of that.        
        
        if subGameState == 5:
            actionText = renderText(fontMainMenu,"Saving....",WHITE)
            if gameTimer < time.get_ticks():
                subGameState = 0
            screen.blit(dimScreen,eScreen)
            screen.blit(actionText,getAlteredImage(actionText,(500,350),"center"))
        else:
            if gameTimer > time.get_ticks():
                draw.rect(screen,GREY,(150,100,700,80))
                alert = renderText(fontButton,"Energy not sufficient for Operation",RED)
                screen.blit(alert,getAlteredImage(alert,(500,140),"center"))        
    
################################################ Story Mode Results Screen ################################################################    
    
    elif gameState == 5:        #players results screen after finishing an expedition for story mode
        screen.blit(field1,eScreen)     #blitting the background
        
        draw.rect(screen,GREY,(150,100,700,400))    #drawing the background window
        
        for x in range(len(resultsRectList)):       #going through all of the text that needs to be drawn
            if pStatus:                             #checking if the player survived or died
                if resultsTextWinList[x] == "titleMessage":         #rendering text for the top menu, depending if the player survives
                    tempText = renderText(fontButton,"You Returned Successfully!",WHITE)    #rendering a congrats
                elif resultsTextWinList[x] == "amt":                #if the text is amt, then get the amount of fuel recieved
                    tempText = renderText(fontButton,str(int(pCurrentCapacity))+" tons of fuel",WHITE)   #rendering the text
                elif resultsTextWinList[x] == "eng":                #if the text calls for the energy gained
                    if pCurrentCapacity == 0:
                        tempText = renderText(fontInfo,"You really came back with no fuel at all?",WHITE)    
                    elif pCurrentCapacity <= 3:
                        tempText = renderText(fontInfo,"Must have been unlucky getting the right asteroids.",WHITE) 
                    elif pCurrentCapacity <= 6:
                        tempText = renderText(fontInfo,"That was a pretty successful run right there.",WHITE)                         
                    else:
                        tempText = renderText(fontInfo,"Impressive haul you got there",WHITE)                     
                    #displays the passive energy gain that happened during the journey
                else:
                    tempText = renderText(fontInfo,resultsTextWinList[x],WHITE)     #default text
                
            else:                                                                   #if the player was hit/destroyed
                if resultsTextLoseList[x] == "titleMessage":                        #if the text calls for the message
                    tempText = renderText(fontButton,"Unfortunately, You Crashed.",LIGHTRED)    #this needs to be red,so it cant be in list
                elif resultsTextLoseList[x] == "amt":                               #if the text calls for the amount of fuel
                    tempText = renderText(fontButton,str(int(pCurrentCapacity/4))+" tons of fuel",WHITE)     #rendering text
                elif resultsTextWinList[x] == "eng":                                #if the text calls for passive energy gain
                    if pCurrentCapacity == 0:
                        tempText = renderText(fontInfo,"Seems like that expedition was pretty rough.",WHITE)    
                    elif pCurrentCapacity <= 2:
                        tempText = renderText(fontInfo,"Atleast we were able to get some fuel out of this run.",WHITE) 
                    else:
                        tempText = renderText(fontInfo,"What a shame, that was looking like a pretty good run.",WHITE) 
                        
                else:                                                               #if there is no modifiers for the text
                    tempText = renderText(fontInfo,resultsTextLoseList[x],WHITE)    #render default text
            
            screen.blit(tempText,getAlteredImage(tempText,resultsRectList[x],"center")) #blits the text onto the screen
        
        returnButton = Rect(330,530,340,60)                                 #making a rect for the button
        returnText = renderText(fontButton,"Go Back to Base",WHITE)         #rendering the text
        if returnButton.collidepoint(mouseCoord):                           #if the mouse is hovering over it
            draw.rect(screen,DARK_GREY,returnButton)                        #draw the button with a darker tone
            if click:                                                       #if a click is detected
                click = False                                               #set the click bool to false
                gameState = 4                                               #set the game state to the menu
                subGameState = 0                                            #set the sub game state to 0 to prevent any problems
                gameTimer = 0                                               #reset the game timer to prevent it from triggering stuff
                pCurrentCapacity = 0
                #pStoredEnergy += baseUpgraded[1]*5+baseUpgraded[2]*500
                resetPlayerStats()
        else:
            draw.rect(screen,GREY,returnButton)                             #draws the normal button if there is no interaction
        screen.blit(returnText,getAlteredImage(returnText,returnButton.center,"center"))    #blitting the text centered.
        
        
######################################################## Creating New Save Name #######################################################
    elif gameState == 6:
        screen.blit(titleImage,eScreen)
        
        for x in range(len(keyPressed)-1,-1,-1): #handling the text input from player
            if keyPressed[x] == '\x08': #if the backspace key is pressed
                if len(pName) > 0:        #if there more than 0 characters in the string to prevent crashing
                    pName = pName[:-1]  #removes the last letter
            elif keyPressed[x] == ',':      #prevents the user from having a comma in their name to prevent errors
                none = False                #meaningless variable
            elif len(pName) >= 16:        #preventing the user from having a very long name
                none = False
            elif keyPressed[x] == '\r':
                if len(pName) > 0:
                    needKey = False
                    updateSaveFile(saveFileIndex)
                    subGameState = 5
                    gameState = 4
                    gameTimer = time.get_ticks() + 500
            else:
                pName += keyPressed[x]    #if nothing preventing user from inputting the current key, add to string.
            keyPressed.pop()                #removes the current key        
        
        namePlate = draw.rect(screen,WHITE,(250,400,500,60))        #
        draw.rect(screen,GREY,(150,100,700,100))
        
        for x in range(len(getNameRectList)):           #going through all of the rects in the list
            if getNameTextList[x] == "name":                    #if the text calls for name
                tempText = renderText(fontButton,pName,BLACK)   #renders the text of the player name
                screen.blit(tempText,getAlteredImage(tempText,getNameRectList[x].move(5,5).topleft,"left"))
                #this gets blit here because it is not a button, and each text in the list has to be placed differently
            elif getNameTextList[x] == "Confirm":               #if the text is confirm
                tempText = renderText(fontButton,getNameTextList[x],WHITE)  #rendering the text
                if getNameRectList[x].collidepoint(mouseCoord):             #checking if the mouse is hovering over it
                    draw.rect(screen,DARK_GREY,getNameRectList[x])          #drawing the background for the button as dark
                    if click:                                               #if a click was detected
                        click = False                                       #set the click to false to prevent issues
                        needKey = False                                     #prevents any more key inputs from being logged
                        updateSaveFile(saveFileIndex)                       #calls the function to update the save file
                        subGameState = 5                                    #changing the state and substate
                        gameState = 4
                        gameTimer = time.get_ticks() + 500                  #updating the timer for when they switch states
                else:
                    draw.rect(screen,GREY,getNameRectList[x])               #drawing the button unselected
                #blitting the button text
                screen.blit(tempText,getAlteredImage(tempText,getNameRectList[x].center,"center"))    
                
                      
            else:   #for the text that does not need any modifiers
                draw.rect(screen,GREY,getNameRectList[x])    #drawing the background for the etxt            
                tempText = renderText(fontButton,getNameTextList[x],WHITE)  #rendering the text
                screen.blit(tempText,getAlteredImage(tempText,getNameRectList[x].center,"center"))  #blitting the text to the screen
                
            
    display.flip()      #updating the screen
    fpsClock.tick(40)   #sestting the max frame rate to 40
    
display.flip()
time.wait(3000)
quit()
