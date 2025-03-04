
class DriveMotorAssembly:
    def __init__(self, wheelRadius, motorL:standardMotor, motorR:standardMotor, hub:PrimeHub, accCalc:AccalerationCalculation, wheelSpacing, gyro:GyroSensor, standardAccSpeeds, DegPerSecToMotorspeed = 1/9.3):
        self.cmPerDeg = (2*3.14159265359 * wheelRadius) / 360
        self.degPerCm = 1 / self.cmPerDeg
        self.motorL = motorL
        self.motorR = motorR
        self.hub = hub  # initiated to be able to use the gyro sensor
        self.gyro = gyro
        self.accCalc = accCalc
        self.currentSpeed = 0
        self.wheelSpacing = wheelSpacing  # for calculating curves
        self.DegPerSecToMotorspeed = DegPerSecToMotorspeed
        self.angle = 0
        self.standardAccSpeeds = standardAccSpeeds
        
    def driveSteer(self, direction, speed):
        '''
        sets both motors to a speed required to drive specified direction

        direction (float): direction to drive; -100 turn on left wheel; +100 turn on right wheel
        speed (int): positive => forward, negative => backwards; range from -100 to 100 
        '''
        
        speed = BasicFunctions.limit(speed, -100, 100)
        direction = BasicFunctions.limit(direction, -100, 100)

        directionLeft = (speed + direction)
        directionRight = (speed - direction)

        self.motorL.setMotorSpeed(directionLeft)
        self.motorR.setMotorSpeed(directionRight)

        self.currentSpeed = speed

    def getMotorDegrees(self):
        '''
        returns average degrees driven by both motors
        '''
        
        return ((self.motorL.getMotorDegrees()+self.motorR.getMotorDegrees())/2)

    def getMotorDegreesRaw(self):
        '''
        returns average raw degrees driven by both motors
        '''
        
        return ((self.motorL.getMotorDegreesRaw()+self.motorR.getMotorDegreesRaw())/2)

    def driveOff(self, stopaction:str='brake'):
        '''
        stopps both motors with specified stopaction

        stopaction (string): 'brake', 'coast', 'hold'; 
            brake: full stop; 
            coast: turn off power without breaking
            hold: break with blocking motor turning
        '''
        
        self.motorL.stopMotor(stopaction)
        self.motorR.stopMotor(stopaction)

        self.currentSpeed = 0

    def getCurrentSpeed(self):
        '''
        returns current motor speed.
        '''
        
        return (self.currentSpeed)

    def driveStraight(self, distance, maxSpeed, endSpeed = 0, gotAngle = None, accTouple = None):
        '''
        drives straight at the theoretical angle taken from last curve.

        If you use that at the beginning of a run/programm, you have to set gotAngle to you targetAngle. Otherwise, it will drive to 0. That sometimes causes mayhem.

        distance (float): the distance, our robot should drive in centimeter
        maxSpeed (int): is the maximum speed at which the robot should drive. That can't be over 100.
        endspeed (int): speed at which the robot should continue driving when distance compleated; important for decelleration. Decellarates to endspeed.
        gotAngle (int): has to be set if you use a driveStraight at the start of a programm/run; between 0 and 360; relative to world. NOT Robot.
        '''

        if (gotAngle != None):
            self.angle = gotAngle
        if(accTouple == None):
            accTouple = self.standardAccSpeeds
        targetAngle = self.angle
            
        #calculates a multiple of 360 where the following equasion will be true:  abs(a - b - difference(a, b)) <= 180
        actualAngle = self.gyro.getAngle()
        correction = actualAngle - targetAngle
        correction = correction - correction % 360
        diff = actualAngle - targetAngle - correction
        if(diff > 180):
            correction += 360

        forwardFactor = BasicFunctions.sign(distance)
        startDegMotors = self.getMotorDegrees()

        PIDDriveStraight.resetPID(self.gyro.getAngle() - targetAngle - correction)
        self.accCalc.resetCalc(distance * self.degPerCm, maxSpeed, accTouple[0], accTouple[1], self.DegPerSecToMotorspeed, 5, endSpeed)

        while (True):
            angle = self.gyro.getAngle() - targetAngle - correction
            direction = PIDDriveStraight.updatePID(angle)

            #print('angle: ', self.gyro.getAngle(), 'Correction: ', direction)

            AccCalcResult = self.accCalc.updateCalc(self.getMotorDegrees() - startDegMotors, self.currentSpeed)
            #direction = (direction/100)*AccCalcResult

            direction *= forwardFactor

            if (AccCalcResult == 0):
                self.driveSteer(0, self.accCalc.getEndspeed())
                break


            #print('diff: ', diff, ' angle: ', angle, ' actual angle: ', self.gyro.getAngle(), ' correction: ', correction, ' diff updated: ', angle - (self.gyro.getAngle() + correction))

            self.driveSteer(-direction*forwardFactor, AccCalcResult)

    #region motorCurves
    #FIXME motorCurves mostly Outdated!!! (delete?) #NOWWWWW!!!
    def ResetAccelerationCalcCurve(self, angle: float, radius: float, maxSpeed: int = 100, endSpeed: int = 0, accTouple=None):
        '''
        DEPRECIATED

        You have to reset every calculation before you can drive a curve. (in driveCurve() is is already managed) This sets all necessary variables to move on a curvepath.
        Especially the distances, every wheel has to drive, are managed here. And have to be reset for every curve.

        angle (float): the angle(, how far the robot should drive at the cirle,) at which the robot should stand at the end of the curve, relative to its start position; positiv => forward, negative => backwards
        radius (float): The radius of the Circle, the robot drives on; positive => draw circle to the right (therefore forwards drives to forward right), negative => draw circle to the left (therefore forward drives to forward left)
        maxSpeed (int): The highest Speed, the robot should accellerate to
        endSpeed (int): The speed, the robot should decellerate to at the end of the curve
        decelerationSpeed (float): speed at which the robot should break; lower is slower, higher is faster
        accelerationSpeed (float): speed at which the robot should accellerate; lower is slower, higher is faster
        '''

        if(accTouple == None):
            accTouple = self.standardAccSpeeds

        radiusDirection = BasicFunctions.sign(radius)

        leftWheelDistanceDeg = angle * \
            ((pi * ((radius + self.wheelSpacing * .5)
             * radiusDirection)) / 180) * self.degPerCm
        rightWheelDistanceDeg = angle * \
            ((pi * ((radius - self.wheelSpacing * .5)
             * radiusDirection)) / 180) * self.degPerCm

        if (radiusDirection == -1):

            accCalc.resetCalc(rightWheelDistanceDeg, maxSpeed, accTouple[0], accTouple[1], self.DegPerSecToMotorspeed, 10, endSpeed)
            self.curveFactor = leftWheelDistanceDeg/rightWheelDistanceDeg
            self.outerWheel = True  # right Wheel outer one
            self.accCalcResult = self.motorR.getMotorSpeed()

        else:

            accCalc.resetCalc(leftWheelDistanceDeg, maxSpeed, accTouple[0], accTouple[1], self.DegPerSecToMotorspeed, 1, endSpeed)
            self.curveFactor = rightWheelDistanceDeg/leftWheelDistanceDeg
            self.outerWheel = False
            self.accCalcResult = self.motorL.getMotorSpeed()

        # here you could manipulate the i therm.
        driveCorrectionCurve.resetPID(0, 0.04)
        self.AccCalcOffsetRight = self.motorR.getMotorDegreesRaw()
        self.AccCalcOffsetLeft = self.motorL.getMotorDegreesRaw()

    def AccelerationCalcCurve(self):
        '''
        DEPRECIATED

        calculates the speed, the individual motors should travel at any given distance. This function drives the motors too.
        has to be updated in a loop. As long as it returns True, it has to be recalled. If it returns False, it is done driving the, in the ResetAccelerationCalcCurve defined, curve.

        return (bool): True, False
        '''
        
        if (self.outerWheel):
            accCalcResult = accCalc.updateCalc(
                self.motorR.getMotorDegreesRaw() - self.AccCalcOffsetRight, self.currentSpeed)
            self.currentSpeed = accCalcResult
            if (accCalcResult == 0):
                self.driveSteer(0, accCalc.getEndspeed())
                return False
            else:
                deviationCorrection = driveCorrectionCurve.updatePID((self.motorR.getMotorDegreesRaw(
                ) - self.AccCalcOffsetRight) * self.curveFactor - (self.motorL.getMotorDegreesRaw() - self.AccCalcOffsetLeft))
                self.motorR.setMotorSpeed(
                    accCalcResult - abs(deviationCorrection) - deviationCorrection)
                self.motorL.setMotorSpeed(
                    (accCalcResult - abs(deviationCorrection) + deviationCorrection)*self.curveFactor)
        else:
            accCalcResult = accCalc.updateCalc(
                self.motorL.getMotorDegreesRaw() - self.AccCalcOffsetLeft, self.currentSpeed)
            self.currentSpeed = accCalcResult
            if (accCalcResult == 0):
                if (accCalc.getEndspeed() == 0):
                    self.driveOff()
                else:
                    self.driveSteer(0, accCalc.getEndspeed())
                return False
            else:
                deviationCorrection = driveCorrectionCurve.updatePID((self.motorL.getMotorDegreesRaw(
                ) - self.AccCalcOffsetLeft) * self.curveFactor - (self.motorR.getMotorDegreesRaw() - self.AccCalcOffsetRight))
                self.motorL.setMotorSpeed(
                    (accCalcResult - abs(deviationCorrection) - deviationCorrection))
                self.motorR.setMotorSpeed(
                    (accCalcResult - abs(deviationCorrection) + deviationCorrection)*self.curveFactor)
        return True

    def driveCurve(self, angle: float, radius: float, maxSpeed: int = 100, endSpeed: int = 0, accTouple=None):
        '''
        DEPRECIATED

        packs a ResetAccelerationCalcCurve and the AccelerationCalcCurve functions into one. (for userfriendlyness)
        you can copy this function into your code to do something in paralell. (then put your code for running parallel in the while loop)

        same inputs as ResetAccelerationCalcCurve. So look there for explanation.
        '''

        if(accTouple == None):
            accTouple = self.standardAccSpeeds

        self.ResetAccelerationCalcCurve(angle, radius, maxSpeed, endSpeed, accTouple)
        self.angle += angle*BasicFunctions.sign(radius)

        while (self.AccelerationCalcCurve()):
            pass

    def driveCurveCm(self, distance, radius, maxSpeed=100, endSpeed=0, accTouple=None):
        '''
        DEPRECIATED

        calculates an angle from a given distance and radius for a normal curve. just passes the values forward and calculates an angle.
        This function is practical for a really large radius. (where you nearly drive straight.)

        distance (float): the distance, the robot should drive on the circle
        other Parameters: look at driveCurve()
        '''
        
        if(accTouple == None):
            accTouple = self.standardAccSpeeds

        angle = (distance * 180) / (pi * abs(radius))
        self.driveCurve(angle, radius, maxSpeed, endSpeed, accTouple)
    
    #endregion motorCurves

    def setGyroPos(self, angle=0):
        '''
        sets the angle of the Robot.
        we do that here and not in the GyroSensorClass, because we have this theoretical value in our DriveMotorAssembly, which is really important to reset too.
        So we can do that here way more easily

        takes an angle (int) to set everything to.

        You use this function at the start of every run, to tell the robor, where it is facing. And if you want to make shure it really knows where it is, you can use it inside the run, when you align the robot with a wall or a mission model.
        '''

        self.angle = angle
        self.gyro.resetYawAngle(angle)
        print('Gyro Pos Set To:      ', self.gyro.getAngle(), self.angle)
    
    def driveLineWithColor(self, distance, maxSpeed, colorSensor, rightSide=1, colorToAngle=3, gotAngle=None, colorChannel=0, endSpeed=0, accTouple=None):
        '''
        here we calculate where on gray we are for linefollowing. if more to white or black, to be able to controll the PID a bit better.
        but this doesn't really work with the Lego Spike Prime color sensor. we just get 6 millimeter readout for gray. This is simply not enough for an PID linefollower.

        Parameters should be self explenatory; colorSensor, should get a ColorSensorClass object from you.
        for explanation of other Params, ask alpha. They are to long to describe in this small text.
        '''

        if (not gotAngle == None):
            sollAngle = gotAngle
        else:
            sollAngle = self.gyro.getAngle()

        if(accTouple == None):
            accTouple = standardAccSpeeds

        forwardFactor = BasicFunctions.sign(distance)

        startDegMotors = self.getMotorDegrees()

        PIDDriveStraight.resetPID(0)
        self.accCalc.resetCalc(distance * self.degPerCm, maxSpeed, accTouple[0], accTouple[1], self.DegPerSecToMotorspeed, 5, endSpeed)

        # definetly do NOT use an integral f the light sensor here, it just desn't work and your code is fine as is
        # ~Delta

        colorDeviationSum = 0

        angles = []

        while (True):
            actualAngle = self.gyro.getAngle()
            modifyer = ((colorSensor.getValue(colorChannel) - valueColorRefThreshold) / valueColorScaleFactor * colorToAngle)
            angle = actualAngle - sollAngle + \
                modifyer * BasicFunctions.sign(rightSide)
            direction = PIDDriveStraight.updatePID(angle)

            colorDeviationSum += modifyer + PIDDriveStraight.deltaTime
            angles.append(actualAngle)
            AccCalcResult = self.accCalc.updateCalc(
                self.getMotorDegrees() - startDegMotors, self.currentSpeed)

            direction = direction * AccCalcResult / 100
            if (AccCalcResult == 0):
                endSpeed = self.accCalc.getEndspeed()

                self.driveSteer(0, endSpeed)
                break

            self.driveSteer(-direction*forwardFactor, AccCalcResult)

        for i in range(len(angles)):
            print(angles[i])

    def driveCurveAbsolute(self, absAngle, radius, backwards: bool, maxSpeed=100, endSpeed=0, accTouple=None):
        '''
        this is a curve to drive to a targetAngle relative to the outer world. and not relative to the robot itself, like the other curves we had so far.
        the absAngle is short for AbsoluteAngle. So relative to the gamemat. (north = 0, east = 90 or -270, south = +-180, west = 270 or -90)

        backward (bool): is used for defining if whether the robot should drive the long or the short way to its goal. So backwards = False will always drive forwards to its destinationAngle
        the other Parameters are pretty much self explanatory
        '''
        
        if(accTouple == None):
            accTouple = self.standardAccSpeeds

        angle = (BasicFunctions.sign(radius) * (absAngle - self.angle)) % 360 - (360 * backwards)
        if(absAngle == self.angle):
            angle = 0
        self.gyroCurve(
            angle,
            radius,
            maxSpeed,
            endSpeed,
            accTouple
        )

    def driveOnLine(self, distance, maxSpeed, sensor:ColorSensorClass, leftSide:bool, endSpeed=0, gotAngle=None, accTouple=None):
        '''
        This function uses our ability to look for different colors coupled with a driveStraight. So we can drive on a line. 
        for more details you can ask alpha. He can explain the idea behind that to you.
        But you basically just need to know that this follows a line (black|White).

        sensor (ColorSensorClass): is the color sensor with which you follow a line
        leftSide (bool): specifies the side of the line. Whether it should steer left or right on the black part of a line.
        you can find all the other Parameters in the driveStraight function.
        '''

        if(accTouple == None):
            accTouple = self.standardAccSpeeds

        if (gotAngle != None):
            self.angle = gotAngle

        sollAngle = self.angle

        forwardFactor = BasicFunctions.sign(distance)

        startDegMotors = self.getMotorDegrees()

        PIDDriveStraight.resetPID(0)
        self.accCalc.resetCalc(distance * self.degPerCm, maxSpeed, accTouple[0], accTouple[1], self.DegPerSecToMotorspeed, 5, endSpeed)

        while (True):
            modifyer = 0

            if(sensor.isBlack()):
                modifyer = 10 * (not leftSide * -1)
            if(sensor.isColor()):
                modifyer = -10 * (not leftSide * -1)

            #print('white: ', ScolS.isWhite(), ' black: ', ScolS.isBlack(), 'color: ', ScolS.isColor())
            angle = self.gyro.getAngle()-sollAngle
            direction = PIDDriveStraight.updatePID(angle) + modifyer

            AccCalcResult = self.accCalc.updateCalc(
                self.getMotorDegrees() - startDegMotors, self.currentSpeed)

            direction = (direction/100)*AccCalcResult
            if (AccCalcResult == 0):
                self.driveSteer(0, self.accCalc.getEndspeed())
                break

            self.driveSteer(-direction*forwardFactor, AccCalcResult)


    #region gyroCurve
    #TODO calculate edge-cases (the ones, which make us still use motorCurves)
    def resetGyroCurve(self, angle: float, radius: float, maxSpeed: int = 100, endSpeed: int = 0, accTouple=None):
        '''
        You have to reset every calculation before you can drive a curve. (in driveCurve() is is already managed) This sets all necessary variables to move on a curvepath.
        Especially the distances, every wheel has to drive, are managed here. And have to be reset for every curve.

        angle (float): the angle(, how far the robot should drive at the cirle,) at which the robot should stand at the end of the curve, relative to its start position; positiv => forward, negative => backwards
        radius (float): The radius of the Circle, the robot drives on; positive => draw circle to the right (therefore forwards drives to forward right), negative => draw circle to the left (therefore forward drives to forward left)
        maxSpeed (int): The highest Speed, the robot should accellerate to
        endSpeed (int): The speed, the robot should decellerate to at the end of the curve
        decelerationSpeed (float): speed at which the robot should break; lower is slower, higher is faster
        accelerationSpeed (float): speed at which the robot should accellerate; lower is slower, higher is faster
        '''

        if(accTouple == None):
            accTouple = self.standardAccSpeeds
        self.radius=radius
        self.radiusDirection = BasicFunctions.sign(radius)

        if(self.radiusDirection == -1):
            self.outerCurveMotor = self.motorR
            self.innerCurveMotor = self.motorL
        else:
            self.outerCurveMotor = self.motorL
            self.innerCurveMotor = self.motorR


        outerWheelDistanceDeg = angle * ((pi * ((radius + self.wheelSpacing * self.radiusDirection * .5) * self.radiusDirection)) / 180) * self.degPerCm
        innerWheelDistanceDeg = angle * ((pi * ((radius - self.wheelSpacing * self.radiusDirection * .5) * self.radiusDirection)) / 180) * self.degPerCm

        accCalc.resetCalc(outerWheelDistanceDeg, maxSpeed, accTouple[0], accTouple[1], self.DegPerSecToMotorspeed, 1, endSpeed)
        self.curveFactor = innerWheelDistanceDeg / outerWheelDistanceDeg

        self.accCalcResult = self.outerCurveMotor.getMotorSpeed()

        gyroCurvePID.resetPID(0)
        self.AccCalcOffsetRight = self.outerCurveMotor.getMotorDegreesRaw()
        self.AccCalcOffsetLeft = self.innerCurveMotor.getMotorDegreesRaw()

        self.curveDistance = outerWheelDistanceDeg
        self.startAngle = self.angle #self.gyro.getAngle()
        self.endAngle = self.angle + angle * self.radiusDirection

    def updateGyroCurve(self):
        '''
        calculates the speed, the individual motors should travel at any given distance. This function drives the motors too.
        has to be updated in a loop. As long as it returns True, it has to be recalled. If it returns False, it is done driving the, in the ResetAccelerationCalcCurve defined, curve.

        return (bool): True, False
        '''
        
        outerMotorDegsRaw = self.outerCurveMotor.getMotorDegreesRaw()
        innerMotorDegsRaw = self.innerCurveMotor.getMotorDegreesRaw()

        self.accCalcResult = accCalc.updateCalc(outerMotorDegsRaw - self.AccCalcOffsetRight, self.currentSpeed)
        self.currentSpeed = self.accCalcResult
        #print(self.accCalcResult, outerMotorDegsRaw - self.AccCalcOffsetRight)
        if (self.accCalcResult == 0):
            self.driveSteer(0, accCalc.getEndspeed())
            return False

        outerMotorOffset = outerMotorDegsRaw - self.AccCalcOffsetRight
        innerMotorOffset = innerMotorDegsRaw - self.AccCalcOffsetLeft


        angle = self.gyro.getAngle()
        distance = outerMotorOffset
        theoreticalAngle = BasicFunctions.remap(distance, 0, self.curveDistance, self.startAngle, self.endAngle)
        deviationCorrection=0

        deviation = angle - theoreticalAngle
        #print(deviation)
        
        #TODO denken ob das gut ist, eventuell 2 arten von kurven?
        if abs(self.radius)>self.wheelSpacing/2:
            deviationCorrection = gyroCurvePID.updatePID(deviation) * self.radiusDirection

        outerSpeed = self.accCalcResult - deviationCorrection
        innerSpeed =self.accCalcResult * self.curveFactor + deviationCorrection 

        self.outerCurveMotor.setMotorSpeed(outerSpeed)
        self.innerCurveMotor.setMotorSpeed(innerSpeed)

        #print('distance: ', distance, 'angle: ', angle, 'theoreticalAngle: ', theoreticalAngle, 'deviation: ', angle-theoreticalAngle)

        return True

    def gyroCurve(self, angle: float, radius: float, maxSpeed: int = 100, endSpeed: int = 0, accTouple=None):
        '''
        packs a ResetAccelerationCalcCurve and the AccelerationCalcCurve functions into one. (for userfriendlyness)
        you can copy this function into your code to do something in paralell. (then put your code for running parallel in the while loop)

        same inputs as ResetAccelerationCalcCurve. So look there for explanation.
        '''
        
        if(accTouple == None):
            accTouple = self.standardAccSpeeds

        self.resetGyroCurve(angle, radius, maxSpeed, endSpeed, accTouple)
        self.angle += angle * BasicFunctions.sign(radius)
        while (self.updateGyroCurve()):
            pass

    def gyroCurveCm(self, distance, radius, maxSpeed=100, endSpeed=0, accTouple=None):
        '''
        calculates an angle from a given distance and radius for a normal curve. just passes the values forward and calculates an angle.
        This function is practical for a really large radius. (where you nearly drive straight.)

        distance (float): the distance, the robot should drive on the circle
        other Parameters: look at driveCurve()
        '''
        
        if(accTouple == None):
            accTouple = self.standardAccSpeeds

        angle = (distance*180)/(pi *  abs(radius))
        self.gyroCurve(angle, radius, maxSpeed, endSpeed, accTouple)

    #endregion gyroCurve

    def driveCurveSpotGyro(self, angle, speed):
        '''
        cause alpha couldn't be bothered to describe anything here I (Omega) have to do it on my own. This SpotCurve is ABSOLUTE, the first value is the absolut angle, the second value is the SPEED and the DIRECTION: + = right/- = left.
        Lastly I want to thank alpha for his colaboration with this (he absolutely isn't annoying us right now) 
        '''
        self.angle = angle
        actualAngle = self.gyro.getAngle()
        angleDif = (angle - actualAngle) % 360

        correction = angle - actualAngle
        correction = correction - correction % 360

        if BasicFunctions.sign(speed) == -1:
            correction += 360
        
        diff = angle - (actualAngle + correction)

        driveMotors.driveSteer(speed, 0)
        if diff > 0:
            while angle - (self.gyro.getAngle() + correction) > 0:
                pass
                #print('diff: ', diff, ' angle: ', angle, ' actual angle: ', self.gyro.getAngle(), ' correction: ', correction, ' diff updated: ', angle - (self.gyro.getAngle() + correction))
        else:
            while angle - (self.gyro.getAngle() + correction) < 0:
                pass
                #print('diff: ', diff, ' angle: ', angle, ' actual angle: ', self.gyro.getAngle(), ' correction: ', correction, ' diff updated: ', angle - (self.gyro.getAngle() + correction))
        driveMotors.driveOff()

    def saveStandardAccSpeeds(self):
        self.savedAccTouple = self.standardAccSpeeds

    def loadStandardAccSpeeds(self):
        self.standardAccSpeeds = self.savedAccTouple

    def setAccSpeeds(self, accSpeed, deAccSpeed):
        self.standardAccSpeeds = (deAccSpeed, accSpeed)
