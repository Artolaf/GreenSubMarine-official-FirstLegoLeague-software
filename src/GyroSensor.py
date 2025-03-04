
class GyroSensor:
    def __init__(self, hub:PrimeHub):
        self.hub = hub
        self.turnValue = -self.getYawAngle()
        self.angleLast = -self.turnValue
        self.resetYawAngle()

    def resetYawAngle(self, offset = 0):
        self.update()
        self.turnValue = -self.getYawAngle() + offset

    def getYawAngle(self):
        return self.hub.motion_sensor.get_yaw_angle()

    def update(self):
        self.angleCurrent = self.getYawAngle()

        if (self.angleLast - self.angleCurrent > 180):
            self.turnValue += 360
        elif (self.angleLast - self.angleCurrent < -180):
            self.turnValue -= 360

        self.angleLast = self.angleCurrent
        return self.turnValue + self.angleCurrent

    def getAngle(self):
        return self.update()
