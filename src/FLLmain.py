# LEGO type:standard slot:0 autostart

#region imports
from spike import PrimeHub, LightMatrix, Button, StatusLight, MotionSensor, Speaker, ColorSensor, App, Motor, MotorPair, ForceSensor, DistanceSensor
import time
from spike import *
from hub import battery

import random
from math import *

#endregion imports

#region standardValues
valueColorRefBlack = 150
valueColorRefWhite = 1024
valueColorRefThreshold = (valueColorRefBlack + valueColorRefWhite) / 2
valueColorScaleFactor = valueColorRefThreshold - valueColorRefBlack
#endregion standardValues

#region libs
from BasicRobotFunctions import *
from BasicFunctions import *
from PIDController import *
from PIDIdecay import *
from StandardMotor import *
from ColorSensorClass import *
from GyroSensor import *
from ForceSensorClass import *
from AccalerationCalculation import *
from DriveMotorAssembly import *
from DistanceSensorClass import *

#region miscellaneous

def varivari(variable, description):    #TODO update varivari / craft better UI
    '''
        variable change during programm
    '''
    step = 1
    print('changing', description, 'now. By ', step, ' step a time.')
    print(variable)
    while True:
        if (basicRoboFunctions.checkButton("right")):
            pressStartTime = BasicFunctions.timeSec()
            while (basicRoboFunctions.checkButton("right")):
                if(BasicFunctions.timeSec() - pressStartTime > 3):
                    basicRoboFunctions.beep()
            if (BasicFunctions.timeSec() - pressStartTime < .5):
                variable += step  # short right; set value
                print(variable)

            elif (BasicFunctions.timeSec() - pressStartTime > 3):
                return variable  # break; done

            else:
                step *= 10  # long right; set interval bigger
                print('changing by ', step, ' now.')

        if (basicRoboFunctions.checkButton("left")):
            pressStartTime = BasicFunctions.timeSec()
            while (basicRoboFunctions.checkButton("left")):
                pass
            if (BasicFunctions.timeSec() - pressStartTime < .5):
                variable -= step  # short left; set value
                print(variable)
            else:
                step *= .1  # long left; set interval smaller
                print('changing by ', step, ' now.')

def getRoboPlotData():
    '''
        returns data used for roboplot.py
    '''
    lastMotorDegs = None
    driveMotors.driveSteer(0, 10)
    while (driveMotors.getMotorDegrees() * driveMotors.cmPerDeg < 20):
        red, green, blue, helligkeit = ScolF.getRGBL()
        currentMotorDeg = driveMotors.getMotorDegrees()
        if (not currentMotorDeg == lastMotorDegs):
            lastMotorDegs = currentMotorDeg
            print(currentMotorDeg * driveMotors.cmPerDeg, red + 0.0000001,
                  green + 0.0000001, blue + 0.0000001, helligkeit + 0.0000001)
            # print(driveMotors.getMotorDegrees() / driveMotors.degPerCm)
    driveMotors.driveOff()

#endregion miscellaneous

#endregion libs

#region prestuff

# --------------------------PIDs----------------------------#
#region PIDs

PIDDriveStraight = PIDIdecay(1, 2, .1, .1)              #DriveMotorAssembly.driveStraight()
driveCorrectionCurve = PIDController(.075, .15, .03)    #DriveMotorAssembly.driveCurve()
gyroCurvePID = PIDController(0.55, .2, 0)               #DriveMotorAssembly.gyroCurve()

accCalc = AccalerationCalculation()


# endregion PIDs
# --------------------------hub---------------------------#
#region hub

robotPrimeHub = PrimeHub()
robotPrimeHub.speaker.set_volume(50)
basicRoboFunctions = BasicRobotFunctions(robotPrimeHub)

# endregion hub
# -------------------------sensors-------------------------#
#region sensors
# gyro Sensor
gyroSensor = GyroSensor(robotPrimeHub)

# color Sensor
SensorColorF = ColorSensor('F')
#SensorColorM = ColorSensor('B')
ScolF = ColorSensorClass(SensorColorF)
#ScolM = ColorSensorClass(SensorColorM)

#distanceSensor
'''
distanceSensorOne = DistanceSensor('B')
distSensor = DistanceSensorClass(distanceSensorOne)
'''

# endregion sensors
# --------------------------motors--------------------------#
#region motors
# drive motors
DriveMotorRightLego = Motor('E')
DriveMotorLeftLego = Motor('C')
MdriveL = standardMotor(DriveMotorLeftLego, True)
MdriveR = standardMotor(DriveMotorRightLego, False)

# funktion Motors
MfnkRLego = Motor('A')
MfnkLLego = Motor('D')
MfnkR = standardMotor(MfnkRLego, False)
MfnkL = standardMotor(MfnkLLego, False)

standardAccSpeeds = 50, 50  #touple for deAccSpeed, accSpeed

driveMotors = DriveMotorAssembly(2.775, MdriveL, MdriveR, robotPrimeHub, accCalc, 12, gyroSensor, standardAccSpeeds)

# endregion
# --------------------------resets--------------------------#
#region resets

MdriveL.motor.set_degrees_counted(0)
MdriveR.motor.set_degrees_counted(0)
MfnkR.motor.set_degrees_counted(0)
MfnkL.motor.set_degrees_counted(0)

robotPrimeHub.motion_sensor.reset_yaw_angle()
startTime = BasicFunctions.timeSec()

# endregion resets
# ---------------------start indicator---------------------#
#region ready
print('battery voltage: ', battery.voltage())
if(battery.voltage() < 8000):
    print()
    print('ERROR: BATTERY LEVEL LOW')
    print()
    while(not basicRoboFunctions.checkButton()):
        robotPrimeHub.light_matrix.write('BATTERY LOW')
        basicRoboFunctions.beep(time=100)

robotPrimeHub.status_light.on('green')
driveMotors.setGyroPos(0)
print('ready to start')
print(); print(); print(); print(); print()
basicRoboFunctions.beep(75, .5)
time.sleep(.1)

# endregion

#region lineSqrt
def lineSqr(speed=10, lineFindSpeed=25, colorValue=3, whiteThreshold=800, blackTheshold=500, sensor=ScolF, motorAssembly=driveMotors):
    '''
    one sensor line squaring
    '''

    motorAssembly.driveSteer(0, lineFindSpeed)  # find line
    while (sensor.getValue(colorValue) < whiteThreshold):
        pass
    while (sensor.getValue(colorValue) > blackTheshold):
        pass
    while (sensor.getValue(colorValue) < whiteThreshold):
        pass
    motorAssembly.driveOff()

    motorAssembly.motorR.setMotorSpeed(speed)  # find left point
    motorAssembly.motorL.setMotorSpeed(-speed)
    while (sensor.getValue(colorValue) > blackTheshold):
        pass

    temporary = motorAssembly.motorL.getMotorDegreesRaw()  # calculate left point

    motorAssembly.motorR.setMotorSpeed(-speed)  # find right point
    motorAssembly.motorL.setMotorSpeed(speed)
    while (sensor.getValue(colorValue) < whiteThreshold):
        pass
    while (sensor.getValue(colorValue) > blackTheshold):
        pass

    toTurn = (temporary - motorAssembly.motorL.getMotorDegreesRaw()) / 2  # calculate right point and half to drive to

    motorAssembly.motorR.setMotorSpeed(speed)  # drive to calculated point
    motorAssembly.motorL.setMotorSpeed(-speed)
    while (temporary - motorAssembly.motorL.getMotorDegreesRaw() < toTurn):
        pass
    motorAssembly.driveOff()

    motorAssembly.driveSteer(0, -lineFindSpeed)  # drive back to line
    while (sensor.getValue(colorValue) > blackTheshold):
        pass
    motorAssembly.driveOff()

    motorAssembly.angle = motorAssembly.gyro.getAngle()

# endregion lineSqrt

#endregion prestuff

#region Runs

# ---------------------runs---------------------#

def selectNextRun(currentRun, nextRun):
    robotPrimeHub.light_matrix.write('I')
    driveMotors.driveOff('coast'); MfnkL.stopMotor('coast'); MfnkR.stopMotor('coast')
    while (True):
        if (basicRoboFunctions.checkButton("right")):
            while (basicRoboFunctions.checkButton("right")):
                pass
            robotPrimeHub.light_matrix.off()
            robotPrimeHub.status_light.on('green')
            print('started Run:     ', nextRun.__name__)
            return nextRun()

        elif (basicRoboFunctions.checkButton("left")):
            while (basicRoboFunctions.checkButton("left")):
                pass
            return currentRun


def runBlack():
    teamTaskAmmount = varivari(2, "determines how often, we will trigger the team task")

    print(teamTaskAmmount)

    
    driveMotors.saveStandardAccSpeeds()
    driveMotors.setAccSpeeds(75, 50)
    MfnkR.driveToAbsolute(-30, 50)
    MfnkL.driveToAbsolute(-45, 50)

    basicRoboFunctions.waitButton()

    SensorColorBlack = None
    ScolBlack = None

    #search for ColorSensor on port B
    while(ScolBlack == None):
        try:    
            SensorColorBlack = ColorSensor('B')
            ScolBlack = ColorSensorClass(SensorColorBlack)
            break
        except:
            pass
    robotPrimeHub.status_light.on('black')  #indicator for sensor connected

    MfnkR.driveMotor(360, 100)
    basicRoboFunctions.waitButton()     #load sound mixer attachement
    MfnkR.driveMotor(-360, 100)
    basicRoboFunctions.waitButton()
    driveMotors.driveSteer(0, 20)
    time.sleep(0.5)
    driveMotors.setGyroPos(180)
    driveMotors.driveOff()
    basicRoboFunctions.beep()

    driveMotors.driveStraight(-14, 75)
    driveMotors.driveCurveSpotGyro(-137, 7)
    driveMotors.driveStraight(-30, 50)  #solve audio mixer
    driveMotors.driveStraight(2.5, 75)
    driveMotors.motorR.driveMotor(-5, 75)
    MfnkL.driveMotor(-645, 50)  # load noah
    MfnkL.driveMotor(645, 50)
    driveMotors.driveStraight(18, 75)    #back off of audio mixer
    basicRoboFunctions.beep()


    driveMotors.driveCurveSpotGyro(110, -100)
    MfnkR.driveMotor(360,50)
    driveMotors.driveCurveSpotGyro(90, 7)
    basicRoboFunctions.beep()   #audio mixer back home

    driveMotors.driveStraight(50 - 2.5, 75)
    #driveMotors.driveCurveSpotGyro(45, -80)
    driveMotors.driveCurveSpotGyro(0 , -7)
    MfnkR.setMotorSpeed(-15)
    driveMotors.driveStraight(55, 75) #immersive experience done
    MfnkL.stopMotor()
    basicRoboFunctions.beep()

    driveMotors.driveStraight(-3, 75)
    #driveMotors.driveCurveSpotGyro(-80, -80)
    driveMotors.driveCurveSpotGyro(-90, -7)
    #MfnkR.setMotorSpeed(50)
    driveMotors.driveStraight(30,75)
    basicRoboFunctions.beep()   #looking west - inbetween audio mixer and skateboard

    driveMotors.driveSteer(0, 25)    
    while(not ScolBlack.isWhite()): pass
    while(not ScolBlack.isBlack()): pass
    driveMotors.driveOff()  #on line in fron of scene change
    driveMotors.driveStraight(7, 75)
    driveMotors.driveCurveSpotGyro(-55, 80)
    driveMotors.driveCurveSpotGyro(-45, 10) #in front of scene change
    MfnkR.driveMotor(600,100)

    driveMotors.driveStraight(4.5, 75)
    MfnkR.driveMotor(-570, 50)
    for i in range((teamTaskAmmount - 1) % 3):
        driveMotors.driveSteer(0, -10)
        MfnkR.driveMotor(300, 50)
        driveMotors.driveSteer(0, 15)
        MfnkR.driveMotor(-300, 50)
    MfnkL.driveMotor(20,100)
    driveMotors.driveStraight(-4, 75)
    MfnkR.driveMotor(550, 100)   #load Sam

    driveMotors.driveStraight(-4, 75)
    driveMotors.driveCurveSpotGyro(20, 20)
    driveMotors.driveStraight(-65, 100, 0, None, (75, 100))


    driveMotors.loadStandardAccSpeeds()
    return selectNextRun(runBlack, runWhite)

def runWhite():
    MfnkL.driveToAbsolute(0, 50)                                            #reset Motorplay
    MfnkR.driveToAbsolute(0, 50)
    basicRoboFunctions.waitButton()


    driveMotors.setGyroPos(90)                                              #drive back and set gyro position
    driveMotors.driveStraight(-35, 75, 0, None, (75, 500))
    time.sleep(0.5)


    driveMotors.driveStraight(60, 75)                                       #drive to the banana and solve it


    driveMotors.driveStraight(-25, 75, 0, None, (100, 500))                                      #drive to tower and solve it
    driveMotors.driveCurveAbsolute(47, -10, False)
    driveMotors.driveStraight(62, 75, 50, None, (100, 100))
    driveMotors.driveCurveAbsolute(90, 5.5, False)
    
    driveMotors.driveStraight(13, 75, 15, None, (75, 500))
    time.sleep(0.1)                                                        #stopping and moving again to reset motorplay at the tower
    MfnkR.driveMotor(-900, 40) 
    MfnkL.driveMotor(-45)                                                    #tower done
    
                   
    
    driveMotors.driveStraight(-7, 75, 0, None, (75, 500))
    driveMotors.driveCurveSpotGyro(0, -20)
    driveMotors.driveCurveAbsolute(-77, 20, True, 75)
    driveMotors.driveStraight(-66.5, 75, 0, None, (75, 1000))                                    #push emmely into home zone
    driveMotors.driveStraight(38, 75, 0, None, (75, 500))                  


    driveMotors.driveCurveAbsolute(-138, 15, True, 75)                      #bring Izzy into home zone
    basicRoboFunctions.beep()
    #driveMotors.driveStraight(-1, 75, 40)#, -110)  #yeet izzy
    basicRoboFunctions.beep()
    driveMotors.driveCurveAbsolute(-45, -20, True, 100, 100, (500, 500))
    driveMotors.driveStraight(-20, 100, 100, None, (500, 500))
    basicRoboFunctions.waitButton()
    driveMotors.driveOff()
    
    return selectNextRun(runWhite, runPrinter) 

def runStage():
    driveMotors.saveStandardAccSpeeds()

    driveMotors.standardAccSpeeds = (10000000, 50)  #deacc, acc

    driveMotors.setGyroPos()
    driveMotors.driveStraight(70,100)
    basicRoboFunctions.beep()
    driveMotors.driveStraight(-60,75)

    driveMotors.loadStandardAccSpeeds()


    MfnkR.driveToAbsolute(-350, 10)                     #Ausrichten und motor zurucksetzten
    MfnkL.driveToAbsolute(0, 10)

    return selectNextRun(runStage, runGreen)

def runPrinter():
    driveMotors.setGyroPos(0)
    
    driveMotors.driveStraight(65, 50, 0, None, (1000000, 75))
    time.sleep(.5)
    driveMotors.driveStraight(-50, 60, 0, None, (100000, 75))
    
    return selectNextRun(runPrinter, runStage)

def runGreen():
    MfnkR.driveToAbsolute(-350, 10)                     #Ausrichten und motor zurucksetzten
    MfnkL.driveToAbsolute(0, 10)
    basicRoboFunctions.waitButton()
    driveMotors.driveSteer(0, -25)
    time.sleep(.5)
    driveMotors.setGyroPos()
    driveMotors.driveOff()      
    


    driveMotors.driveStraight(37 + 2, 75, 0, None, (75, 500))
    MfnkR.driveMotor(-30, 20)
    driveMotors.driveCurveSpotGyro(-45, -20)
    driveMotors.driveStraight(32 - 5, 75, 0, None, (75, 500))
    driveMotors.driveCurveSpotGyro(-90, -20)                                   #seitlich zur blume und drucker
                  
    driveMotors.driveStraight(45, 100, 0, None, (75, 500))

    #basicRoboFunctions.waitButton()

    MfnkR.driveMotor(110, 50)
    driveMotors.driveStraight(-45, 100, 0, None, (75, 500))                      
    MfnkR.driveMotor(-100, 50)
    
    
    driveMotors.driveStraight(38 + 2.5, 75, 0, None, (75, 500))                       #Blume ist ausgefuhrt
    MfnkL.setMotorSpeed(-45)                                                       #"Blumenarm" wird eingezogen  
    
                             
    driveMotors.driveCurveAbsolute(0, 15, False, 100)                       #An die Wand fahren und Gyro resetten
    driveMotors.driveSteer(0, 35)
    time.sleep(.33)
    #driveMotors.setGyroPos(0)
    driveMotors.driveOff()
    driveMotors.driveStraight(-7, 75, 0, None, (75, 500))
    MfnkL.stopMotor()    
    MfnkL.driveMotor(-70, -50)                                                       #Museumsmann wird abgesetzt
    
    
    driveMotors.driveCurveAbsolute(90, -15, True, 75, 40, (75, 500))                       #Skateboard 
    driveMotors.driveStraight(-17, 75, 40, None, (75, 500))
    driveMotors.driveCurveAbsolute(180, -15, True, 75, -40)
    driveMotors.driveStraight(5.5, 75, 0, None, (75, 500))
    MfnkR.driveMotor(100, 50)                                           #Izzi wird wegen migrationshintergrund zum skateboard abgeschoben
    
    
    driveMotors.driveCurveAbsolute(-115, 5, False, 50)                            #fahren zum Popkorn
    driveMotors.driveStraight(15, 75)                       
    driveMotors.driveCurveAbsolute(-105, driveMotors.wheelSpacing/2, False, 15)
    driveMotors.driveStraight(3, 25, 0, driveMotors.gyro.getAngle())
    
         
    return runGreen



     
# region ExampleRun
def runExample():
    #example start
    MfnkL.driveToAbsolute(30, 10)
    MfnkR.driveToAbsolute(95, 10)
    basicRoboFunctions.waitButton()

    MfnkR.driveMotor(-180)
    MfnkL.resetMotorDegrees()
    MfnkR.resetMotorDegrees()
    basicRoboFunctions.waitButton()

    driveMotors.setGyroPos(-90)
    MfnkL.driveMotor(-195, 50)
    driveMotors.driveStraight(-25, 100)
    MfnkL.driveMotor(200, 15)  

    #drive
    #single motor
    MfnkL.driveMotor(-200, 50) 
    #motorassamly
    driveMotors.driveStraight(-21, 100) #geradeaus distanz fahren
    driveMotors.driveSteer(50,90) #motoren anschalten (kurve) 
    time.sleep(1) #roboter fahrt 1s
    driveMotors.driveOff()  #motoren stoppen
    #curves
    driveMotors.gyroCurve(45,2)
    driveMotors.gyroCurveCm(100,100)
    driveMotors.driveCurveCm(30,-20)
    driveMotors.driveCurve(-45,50)
    driveMotors.driveCurveAbsolute(180, -driveMotors.wheelSpacing/2, True, 100)
    driveMotors.driveCurveSpotGyro(24,-10)

    #sensors
    ScolF.getRGBL() #list of RGBL measurements
    ScolM.getValue(0) #one of RGBL
    ScolF.isBlack() #bool, exist also for whithe and color

    #drive to line
    driveMotors.driveSteer(0,50)
    while ScolF.isColor(): #solange fahren wie bunt ist
        pass
    while not ScolF.isBlack(): #solange fahren wie nicht schwarz  ist
        pass
    while not ScolF.isWhite(): #solange fahren wie nicht weiss ist
        pass
    driveMotors.driveOff()  #sollte nach schwarz halten

    #linefollow
    #todo

    driveMotors.driveStraight(-8, 100)
    MfnkL.driveMotor(150, 10)   #energy unit
    driveMotors.driveSteer(0, -50)
    time.sleep(1)
    MfnkL.driveMotor(30, 10)
    driveMotors.driveOff()      #hand

    driveMotors.driveCurveAbsolute(-90, 19, False, 100)
    MfnkR.driveMotor(180, 100)
    driveMotors.driveStraight(26, 100, 0)

    for i in range(2):
        MfnkR.driveMotor(-180)
        MfnkR.driveMotor(180)
    MfnkR.driveMotor(-150)   #oil done

    driveMotors.driveCurveAbsolute(0, -.25, True, 10)
    driveMotors.driveStraight(5, 100, 25)
    time.sleep(1)
    driveMotors.driveOff()
    MfnkR.driveMotor(150)   #grab energy trailor
    driveMotors.driveStraight(-8, 50)

    driveMotors.driveCurve(-25, 16, 75)
    MfnkR.driveMotor(-100)   #hydroelectric damm
    time.sleep(.5)
    MfnkR.driveMotor(100)
    
    driveMotors.driveCurveAbsolute(45, -driveMotors.wheelSpacing - 1, True, 100, 15)
    driveMotors.driveStraight(-2, 50, 25)
    driveMotors.driveCurveAbsolute(90, driveMotors.wheelSpacing + 3, False)
    MfnkR.driveMotor(-10)
    driveMotors.driveStraight(-16, 100, 0, None, (70, 150))
    driveMotors.driveStraight(-12.5, 25)  #oil truck

    driveMotors.driveStraight(10, 100, 50)
    driveMotors.driveCurveAbsolute(30, -20, False)
    driveMotors.driveStraight(-70, 100)

    time.sleep(2)
    MfnkL.driveToAbsolute(45, 50)
    MfnkR.driveToAbsolute(45, 50)

    #return selectNextRun(runCurrent, runNext) #end of run

#endregion ExampleRun

#endregion Runs



#region Main
# ---------------------------Code---------------------------#


selectedRun = 0

runList = [runBlack, runWhite, runPrinter, runStage, runGreen]
colorList = ['blue', 'white', 'orange', 'violet', 'green']

def drawProgressBar(value):
    robotPrimeHub.light_matrix.off()
    for i in range(value):
        robotPrimeHub.light_matrix.set_pixel(i // 5, i % 5, 50)
    robotPrimeHub.light_matrix.set_pixel(value // 5, value % 5, 100)

def updateUI(selectedRun):
    robotPrimeHub.status_light.on(colorList[selectedRun])
    drawProgressBar(selectedRun)

updateUI(selectedRun)

while (True):
    if (basicRoboFunctions.checkButton("right")):
        buttonPressStartTime = BasicFunctions.timeSec()
        while basicRoboFunctions.checkButton("right"):
            pass
        if (BasicFunctions.timeSec() - buttonPressStartTime < .5):
            robotPrimeHub.light_matrix.off()
            robotPrimeHub.status_light.on('green')
            print('started Run:     ', runList[selectedRun].__name__)
            selectedRun = runList.index(runList[selectedRun]())

        else:
            selectedRun = (selectedRun + 1) % len(runList)
        updateUI(selectedRun)

    elif (basicRoboFunctions.checkButton("left")):
        while basicRoboFunctions.checkButton("left"):
            pass
        selectedRun = (selectedRun - 1) % len(runList)
        updateUI(selectedRun)

# -------------------------end------------------------------#
driveMotors.driveOff('brake')
MfnkR.stopMotor('brake')
MfnkL.stopMotor('brake')

raise RuntimeError('intentional abort (end of programm)')

#endregion Main