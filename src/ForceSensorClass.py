
class ForceSensorClass:
    def __init__(self, forceSensorLego:ForceSensor):
        self.sensor = forceSensorLego

    def getStatus(self, index=0):  
        '''
            0 = pressed; 1 = force in newton; 2 = force in percent
        '''
        if (index == 0):
            return self.sensor.is_pressed()
        elif (index == 1):
            return self.sensor.get_force_newton()
        else:
            return self.sensor.get_force_percentage()
