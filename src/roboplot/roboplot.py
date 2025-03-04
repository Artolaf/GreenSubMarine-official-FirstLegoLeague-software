import matplotlib.pyplot as plt
import numpy as np

f = open(r'slkdfhjkl.txt', 'r')
values = f.read()
values = values.split('\n')

preSplitValues = []

for i in values:
    preSplitValues.append(i.split())



splitValues = preSplitValues

motors = []
red = []
green = []
blue = []
luminecence = []

for i in range(len(splitValues)):
    motors.append(float(splitValues[i][0]))
    red.append(float(splitValues[i][1]))
    green.append(float(splitValues[i][2]))
    blue.append(float(splitValues[i][3]))
    luminecence.append(float(splitValues[i][4]))

#print(motors)
plt.plot(motors, red, 'r-', motors, green, 'g-', motors, blue, 'b-', motors, luminecence, 'p-')
plt.axis([0, 20, 0, 1024])
plt.xticks(np.arange(0, 20, step=2))
plt.show()