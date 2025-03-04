

class AccalerationCalculation:
    def __init__(self):
        self.motorMaxSpeed = 100
        self.minSpeed = 5

    def resetCalc(self, _distanceDeg: int, maxSpeed, decelerationSpeed, accelerationSpeed, DegPerSekToMotorspeed, minSpeed=5, _endSpeed: int = 0):
        self.DegPerMsToMotorspeed = DegPerSekToMotorspeed

        self.endSpeed = abs(_endSpeed)
        self.distanceDeg = abs(_distanceDeg)

        self.forwardFactor = BasicFunctions.sign(_distanceDeg)

        self.decelerationSpeed = decelerationSpeed
        self.accelerationSpeed = accelerationSpeed

        self.motorMaxSpeed = maxSpeed
        self.minSpeed = minSpeed

        self.deltaTime = BasicFunctions.timeSec()
        self.lastFrameTime = BasicFunctions.timeSec()
        self.maxSpeedLocal = 0

    def updateCalc(self, currentMotorDegreesFromZero: float, currentSpeed: float):
        if (currentMotorDegreesFromZero * self.forwardFactor >= self.distanceDeg):
            return 0


        self.deltaTime = BasicFunctions.timeSec() - self.lastFrameTime
        self.lastFrameTime = BasicFunctions.timeSec()

        # calculate Deceleration
        maxCurrentSpeed = sqrt(2*self.DegPerMsToMotorspeed*self.decelerationSpeed*(self.distanceDeg-(currentMotorDegreesFromZero) * self.forwardFactor)+(self.endSpeed*self.endSpeed))
        maxSpeedLocal = BasicFunctions.limit(maxCurrentSpeed, self.minSpeed, self.motorMaxSpeed)


        suggestedSpeed = currentSpeed * self.forwardFactor + self.accelerationSpeed * self.deltaTime

        return self.forwardFactor * BasicFunctions.limit(suggestedSpeed, self.minSpeed, maxSpeedLocal)

    def getEndspeed(self):
        return self.endSpeed * self.forwardFactor
