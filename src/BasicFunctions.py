class BasicFunctions:
    def __init__(self):
        pass

    def limit(input: float, min:float, max:float):
        '''
        The limit function return a value clamped between min and max.
        if the value is less than min, it returns min, if value is greater than max, max is being returned, otherwise just the value gets returned

        input : float
          the value you wannt to clamp
        min : float
          lower threshold
        max (float): upper threshold
        return(float): clamped value
        '''

        if (input < min):
            return float(min)
        if (input > max):
            return float(max)
        return float(input)

    def random(min:int, max:int):
        '''
        This function returns a random value(int) between min and max.
        
        min (int): lower value
        max (int): higher limit
        return(int): random value between min and max
        '''

        return (random.randint(min, max))

    def sign(value:float):
        '''
        Returns a -1 if value is negative and 1 if positive

        special case here! 0! Sometimes you want to get another omen then positive for 0...

        value (float): value from which you want to get the omen
        return: -1 or 1
        '''

        if (value < 0):
            return (-1)
        return (1)

    def timeSec()->int:
        '''
        Returns the Time between programm start and fuction call.

        return (int): passed time
        '''

        try:
            timestamp = time.ticks_ms()/1000
        except AttributeError:
            timestamp = time.time_ns() / 1000000000

        return (timestamp)

    def remap(value, low1, high1, low2, high2):
        '''
        Remaps value from reange low1 to low2, to high1, high2.
        (eg. percent is range 0 to 100; color sensor is range 0 to 1024; therefor you could convert color values to percent and the other way around.)
        
        [namesceme low1,2; high1,2:  low is first and gets higher (i guess - alpha)]

        value (number): value to remap
        low1 (number): lowest value range 1
        low2 (number): highest value range 1
        high1 (number): lowest value range 2
        high2 (number): highest value range 2
        return (number): remapped value
        '''

        return low2 + (value - low1) * (high2 - low2) / (high1 - low1)

    def lerp(t, lower, upper):
        '''
        Interpolates between lower and upper at t.

        Drawes imaginary line between lower and upper; returns values at 't'; t = 0 => lower; t = 1 => upper; t = 1/2 => direct middle between lower and upper; used in eg. bezier curves

        t (number): value inbetween 0 and 1; at which you get the interpolation
        lower (number): first (most often lower) interpolation goal
        upper (number): sacond (most often higher) interpolation goal
        return (number): interpolated value
        '''

        return lower + (upper - lower) * t
