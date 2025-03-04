
class PIDIdecay:
    def __init__(self, P, I, D, iDecayPerSec, lowerOutputLimit=-100, upperOutputLimit=100):
        self.P = P
        self.I = I
        self.D = D

        self.resetPID(0)

        self.lowerOutputLimit = lowerOutputLimit
        self.upperOutputLimit = upperOutputLimit

        self.iDecayPerSec = iDecayPerSec

    def setIdecayPerSecond(self, iDecayPerSec):
        self.iDecayPerSec = iDecayPerSec

    def updatePID(self, deviationValue):
        time.sleep(.05)
        self.time = BasicFunctions.timeSec()
        self.deltaTime = self.time - self.lastUpdateTime
        self.lastUpdateTime = self.time

        self.PTherm = self.P * deviationValue

        self.ITherm = BasicFunctions.limit((self.ITherm + deviationValue * self.deltaTime * self.I) * pow(
            self.iDecayPerSec, self.deltaTime), self.lowerOutputLimit, self.upperOutputLimit)

        self.DTherm = (deviationValue - self.lastDeviationValue) * \
            self.D / self.deltaTime

        self.lastDeviationValue = deviationValue

        return (BasicFunctions.limit(self.PTherm + self.ITherm + self.DTherm, self.lowerOutputLimit, self.upperOutputLimit))

    def resetPID(self, deviationValue=0):
        self.PTherm = 0
        self.ITherm = 0
        self.DTherm = 0

        self.lastDeviationValue = deviationValue
        self.lastUpdateTime = BasicFunctions.timeSec()
