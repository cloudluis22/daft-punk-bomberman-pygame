import pygame as pg
import constants

# This class is made for centralizing input logic which makes it easier to add
# more actions and of course to finally implement controller support.

class InputHandler:
    def __init__(self):
        pg.joystick.init()
        self.joysticks = []
        self.deadzone = 0.2
        self.isUsingController = False

        self.key_bindings = {
            pg.K_UP: constants.INPUT_UP,
            pg.K_DOWN: constants.INPUT_DOWN,
            pg.K_LEFT: constants.INPUT_LEFT,
            pg.K_RIGHT: constants.INPUT_RIGHT,

            pg.K_RETURN: constants.INPUT_SELECT,
            pg.K_ESCAPE: constants.INPUT_PAUSE,
            pg.K_SPACE: constants.INPUT_DROP_BOMB,
        }

        self.joy_bindings = {
            0: constants.INPUT_SELECT,
            2: constants.INPUT_DROP_BOMB
        }

        self.actions = {
            constants.INPUT_UP: {"active" : False, "pressed": False},
            constants.INPUT_DOWN: {"active" : False, "pressed": False},
            constants.INPUT_LEFT: {"active" : False, "pressed": False},
            constants.INPUT_RIGHT: {"active" : False, "pressed": False},

            constants.INPUT_SELECT: {"active" : False, "pressed": False},
            constants.INPUT_PAUSE: {"active" : False, "pressed": False},
            constants.INPUT_DROP_BOMB: {"active" : False, "pressed": False},
        }

        # This block of code detects joysticks already connected before game initialization.
        for i in range(pg.joystick.get_count()):
            joy = pg.joystick.Joystick(i)
            self.joysticks.append(joy)
            print(f"Controller {joy.get_name()} already connected!")

    def update(self, events):

        # reset pressing at the beginning so its only true for one loop cycle.
        for action in self.actions:
            self.actions[action]["pressed"] = False

        for event in events:
            if event.type == pg.KEYDOWN:
                self.isUsingController = False
                if event.key in self.key_bindings:
                    action = self.key_bindings[event.key]
                    self.actions[action]["pressed"] = True

            if event.type == pg.JOYBUTTONDOWN:
                self.isUsingController = True
                if event.button in self.joy_bindings:
                    action = self.joy_bindings[event.button]
                    self.actions[action]["pressed"] = True

            if event.type == pg.JOYDEVICEADDED:
                joy = pg.joystick.Joystick(event.device_index)
                self.joysticks.append(joy)
                print(f"Controller: {joy.get_name()} was just connected!")
            
            if event.type == pg.JOYHATMOTION:
                self.isUsingController = True
                x, y = event.value
                if x == -1: 
                    self.actions[constants.INPUT_LEFT]["pressed"] = True
                    self.actions[constants.INPUT_LEFT]["active"] = True
                elif x == 1: 
                    self.actions[constants.INPUT_RIGHT]["pressed"] = True
                    self.actions[constants.INPUT_RIGHT]["active"] = True
                else: 
                    self.actions[constants.INPUT_LEFT]["active"] = False
                    self.actions[constants.INPUT_RIGHT]["active"] = False

                if y == -1: 
                    self.actions[constants.INPUT_DOWN]["pressed"] = True
                    self.actions[constants.INPUT_DOWN]["active"] = True
                elif y == 1: 
                    self.actions[constants.INPUT_UP]["pressed"] = True
                    self.actions[constants.INPUT_UP]["active"] = True
                else: 
                    self.actions[constants.INPUT_UP]["active"] = False
                    self.actions[constants.INPUT_DOWN]["active"] = False

        # Handling continuous input
        if not self.isUsingController:
            keys = pg.key.get_pressed()
            for key, action in self.key_bindings.items():
                self.actions[action]["active"] = keys[key]

    def is_pressed(self, action):
        # returns true only on the exact frame the button is pressed.
        return self.actions.get(action, {}).get("pressed", False)

    def is_active(self, action):
        # returns true as long as it is holding press.
        return self.actions.get(action, {}).get("active", False)
    
    def low_freq_rumble(self):
        for joy in self.joysticks:
            joy.stop_rumble() # stop previous rumbles if happening.
            joy.rumble(0.8, 0.2, 350)

    def high_freq_rumble(self):
        for joy in self.joysticks:
            joy.stop_rumble()
            joy.rumble(0.2, 0.5, 150)
