
class PIDController:    #FIXME without power function (should be faster than PIDIdecay) -> PIDController = PIDIdecay with idecay = 1
    def __init__(self, P, I, D, lowerOutputLimit=-100, upperOutputLimit=100):
        '''
        initialises a PID correction algorythm

        P (number): P correction ammount
        I (number): I correction ammount
        D (number): D correction ammount
        lowerOutputLimit (number): lowest value to correct/output
        upperOutputLimit (number): highest value to correct/output
        '''

        self.P = P
        self.I = I
        self.D = D

        self.resetPID(0)

        self.lowerOutputLimit = lowerOutputLimit
        self.upperOutputLimit = upperOutputLimit

    def updatePID(self, deviationValue):
        '''
        calculates the correction based on the new deviation (and last for I).
        Returns a value which should be applied to correct given deviation.
        
        deviationValue (number): current deviation which should be corrected
        return (number): ammont of correction
        '''

        self.time = BasicFunctions.timeSec()
        self.deltaTime = self.time - self.lastUpdateTime
        self.lastUpdateTime = self.time

        self.PTherm = self.P * deviationValue

        self.ITherm = BasicFunctions.limit((self.ITherm + deviationValue * self.deltaTime * self.I), self.lowerOutputLimit, self.upperOutputLimit)

        if(self.deltaTime != 0):
            self.DTherm = (deviationValue - self.lastDeviationValue) * self.D / self.deltaTime
        else:
            self.DTherm = 0

        self.lastDeviationValue = deviationValue

        #print('P: ', self.PTherm, ' I: ', self.ITherm, ' D: ', self.DTherm)

        return (BasicFunctions.limit(self.PTherm + self.ITherm + self.DTherm, self.lowerOutputLimit, self.upperOutputLimit))

    def resetPID(self, deviationValue=0, startI = 0):
        '''
        resets all PID-Therms and sets first deviation value without correcting. (here just I would be necessary, but all is not wrong)

        deviationValue (number): is the deviation which you want to counteract (correct to 0)
        '''

        self.PTherm = 0
        self.ITherm = startI
        self.DTherm = 0

        self.lastDeviationValue = deviationValue
        self.lastUpdateTime = BasicFunctions.timeSec()
