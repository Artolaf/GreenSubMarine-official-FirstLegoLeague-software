
class standardMotor:
    def __init__(self, motor:Motor, invert:bool = False):
        self.motor = motor
        self.invert(invert)
        self.degreeOffset = self.getMotorDegreesRaw()
        self.currentSpeed = 0

    def invert(self, invert:bool):
        if (invert == True):
            self.invert = -1
        else:
            self.invert = 1

    def applyInvertion(self, input):
        return (input*self.invert)

    def setMotorSpeed(self, speed):
        '''
            speed in %
        '''

        _speed = self.applyInvertion(
            int(BasicFunctions.limit(round(speed), -100, 100)))
        self.motor.start(_speed)
        self.currentSpeed = _speed

    def stopMotor(self, stopaction:str='brake'):
        '''
            stopactions: 'brake', 'coast', 'hold'
        '''

        self.motor.set_stop_action(stopaction)
        self.motor.stop()
        self.currentSpeed = 0

    def setStallDetection(self, enabled: bool):
        '''
            stall detection directly from Lego
            stops motor after 2 sec of not being able to run
        '''

        self.motor.set_stall_detection(enabled)

    def getMotorDegrees(self):
        return (self.getMotorDegreesRaw() - self.degreeOffset)

    def resetMotorDegrees(self, offset = 0):
        self.degreeOffset = self.getMotorDegreesRaw() + self.applyInvertion(offset)

    def getMotorDegreesRaw(self):
        return (self.applyInvertion(self.motor.get_degrees_counted()))

    def driveMotor(self, degrees, speed = 100):
        self.motor.run_for_degrees(self.applyInvertion(degrees), speed)

    def driveToAbsoluteZero(self, speed = 10):
        self.driveToAbsolute(0, speed)

    def driveToAbsolute(self, absoluteDegrees:int, speed = 100):
        self.motor.run_to_position(self.applyInvertion(absoluteDegrees) % 360, 'shortest path', speed)

    def getMotorSpeed(self):
        return self.motor.get_speed()
