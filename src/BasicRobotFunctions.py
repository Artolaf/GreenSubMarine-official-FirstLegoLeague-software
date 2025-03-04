
class BasicRobotFunctions:
    def __init__(self, hub: PrimeHub):
        self.hub = hub

    def waitButton(self, button:str="right"):
        '''
        The waitbutton function waits while the given button is not released.
        It waits, while button is not pressed followed by a wait till our button is released.

        NOTE: You should not wait for 'center'. If you press that, the programm will be terminated... Not really useful.

        button (string): 'right', 'left', 'center'; specifies which hub button the function should wait for. (left is the left one, while hub lays flat on ground and all 3 buttons face down)
        '''

        if button == "left":
            while self.hub.left_button.is_pressed() == False:
                pass
            while self.hub.left_button.is_pressed() == True:
                pass
            return (True)
        if button == "right":
            while self.hub.right_button.is_pressed() == False:
                pass
            while self.hub.right_button.is_pressed() == True:
                pass
            return (True)
        if button == "center":
            while self.hub.center_button.is_pressed() == False:
                pass
            while self.hub.center_button.is_pressed() == True:
                pass
            return (True)

    def checkButton(self, button: str = "right"):
        '''
        This function returns a True(bool) if specified button is pressed. Otherwise returns False(bool).

        button (string): 'left', 'center', right'; button that you want to get the value from
        return (bool): True or False
        '''

        if (button == 'right'):
            if (self.hub.right_button.is_pressed() == True):
                return (True)
            else:
                return (False)

        if (button == 'left'):
            if (self.hub.left_button.is_pressed() == True):
                return (True)
            else:
                return (False)

    def beep(self, note = 90, time = .25):
        self.hub.speaker.beep(note, time)
