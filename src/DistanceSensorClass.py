
class DistanceSensorClass:
    LEDs = [0,0,0,0]

    def __init__(self, sensor):
        self.distSensorLego = sensor

    def setLED(self, index:int, strength:int):
        '''
        sets one of the LEDs of the distanceSensor to a specified strength

        Arguments:
            index: 0 - 3 (spot of LED)
            strength: 0 - 100% brightness
        '''
        if(not index in range(0, 3)):
            raise IndexError("index out of range 0 - 3")

        self.LEDs[index] = strength
        self.drawLEDs()

    def setLEDs(self, brightnessLEDOne, brightnessLEDTwo, brightnessLEDThree, brightnessLEDFour):
        '''
        sets the brightnesses of all LEDs

        Arguments:
            brightnessLED...: brightness in % (0 - 100)
        '''
        self.LEDs = [brightnessLEDOne, brightnessLEDTwo, brightnessLEDThree, brightnessLEDFour]
        self.drawLEDs()

    def drawLEDs(self):
        self.distSensorLego.light_up(self.LEDs[1], self.LEDs[0], self.LEDs[3], self.LEDs[2])

    def getLEDs(self):
        return self.LEDs

    def getDistance(self):
        '''returns distance form DistanceSensor in centimeters'''
        return self.distSensorLego.get_distance_cm()

    def waitForDistance(self, distance:float, farther:bool, shortRange:bool):
        if(farther):
            self.distSensorLego.wait_for_distance_farther_than(distance, 'cm', shortRange)
        else:
            self.distSensorLego.wait_for_distance_closer_than(distance, 'cm', shortRange)
        return
