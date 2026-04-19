import pygame as pg

# This class is made for centralizing input logic which makes it easier to add
# more actions and of course to finally implement controller support.

class InputHandler:
    def __init__(self):
        pg.joystick.init()
        self.joysticks = []
        self.deadzone = 0.2

        self.key_bindings = {
            # SEL bindings are for one time only inputs like for menu and pause
            # screens for example while UP, DOWN etc are for in-game concurrent input.
            pg.K_w: "SEL_UP",
            pg.K_UP: "SEL_UP",
            pg.K_w: "UP",
            pg.K_UP: "UP",

            pg.K_s: "SEL_DOWN",
            pg.K_DOWN: "SEL_DOWN",
            pg.K_s: "DOWN",
            pg.K_DOWN: "DOWN",
    
            pg.K_a: "SEL_LEFT",
            pg.K_LEFT: "SEL_LEFT",
            pg.K_a: "LEFT",
            pg.K_LEFT: "LEFT",

            pg.K_d: "SEL_RIGHT",
            pg.K_RIGHT: "SEL_RIGHT",
            pg.K_d: "RIGHT",
            pg.K_RIGHT: "RIGHT",

            pg.K_RETURN: "SELECT",
            pg.K_SPACE: "DROP_BOMB",
        }

        self.joy_bindings = {

        }

        self.actions = {
            "SEL_UP": False,
            "SEL_DOWN": False,
            "SEL_LEFT": False,
            "SEL_RIGHT": False,

            "UP": False,
            "DOWN": False,
            "LEFT": False,
            "RIGHT": False,

            "SELECT": False,
            "DROP_BOMB": False
        }

        # This block of code detects joysticks already connected before game initialization.
        for i in range(pg.joystick.get_count()):
            joy = pg.joystick.Joystick(i)
            self.joysticks.append(joy)
            print(f"Controller {joy.get_name()} already connected!")

    def update(self):
        # Resetting one time triggers.
        self.actions["SEL_UP"] = False
        self.actions["SEL_DOWN"] = False
        self.actions["SEL_LEFT"] = False
        self.actions["SEL_RIGHT"] = False
        self.actions["SELECT"] = False
        self.actions["DROP_BOMB"] = False

        for event in pg.event.get():

            if event.type == pg.KEYDOWN:
                if event.key in self.key_bindings:
                    self.actions[self.key_bindings[event.key]] = True

            if event.type == pg.JOYDEVICEADDED:
                joy = pg.joystick.Joystick(event.device_index)
                self.joysticks.append(joy)
                print(f"Controller: {joy.get_name()} was just connected!")