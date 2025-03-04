
class ColorSensorClass:
    def __init__(self, sensor:ColorSensor):
        self.sensor = sensor

    def getRGBL(self):
        '''
        get sensor touple
        '''

        return (self.sensor.get_rgb_intensity())

    def getValue(self, number:int):
        number = BasicFunctions.limit(number, 0, 3)
        value0, value1, value2, value3 = self.sensor.get_rgb_intensity()
        if (number == 0):
            return (value0)
        elif (number == 1):
            return (value1)
        elif (number == 2):
            return (value2)
        elif (number == 3):
            return (value3)
        else:
            raise RuntimeError('Value does not exist')

    def isWhite(self):
        red, green, blue, brightness = self.getRGBL()
        rgbsum = red + green + blue
        if (rgbsum > 2850):
            return True

    def isBlack(self):
        red, green, blue, brightness = self.getRGBL()
        rgbsum = red + green + blue

        rgdiv = red - green
        gbdiv = green - blue
        brdiv = blue - red
        rgbdiv = rgdiv * rgdiv + gbdiv * gbdiv + brdiv * brdiv

        if (rgbsum < 2850):
            if (rgbdiv < 35000):
                return True

    def isColor(self):
        '''
            checks for not white and not black
        '''

        red, green, blue, brightness = self.getRGBL()
        rgbsum = red + green + blue

        rgdiv = red - green
        gbdiv = green - blue
        brdiv = blue - red
        rgbdiv = rgdiv * rgdiv + gbdiv * gbdiv + brdiv * brdiv

        if (rgbsum < 2850):
            if (rgbdiv > 35000):
                return True
