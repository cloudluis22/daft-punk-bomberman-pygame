import pygame as pg
import constants

# This class handles screen fade in and out for transition between scenes (e.g. main menu, gameplay)
class TransitionManager():
    def __init__(self):
        self.height = constants.SCREEN_HEIGHT
        self.width = constants.SCREEN_WIDTH

        self.surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.rect = self.surface.get_rect()

        self.state = constants.T_STATE_IDLE
        self.t_alpha = 0

        self.blackoutEventSent = False
    
    def transition_fade_out(self):
        # we reset the blackout event flag here
        if self.state == constants.T_STATE_IDLE:
            self.blackoutEventSent = False
            self.state = constants.T_STATE_FADING_OUT

    def transition_fade_in(self):
        if self.state == constants.T_STATE_BLACKOUT:
            self.blackoutEventSent = False
            self.state = constants.T_STATE_FADING_IN

    def draw_transition(self):
        match self.state:
            case constants.T_STATE_IDLE:
                self.surface.fill((0, 0, 0, 0))
            case constants.T_STATE_BLACKOUT:
                self.surface.fill((0, 0, 0, 255))
                if self.blackoutEventSent == False:
                    event_blackout = pg.event.Event(constants.EV_SCREEN_BLACKOUT)
                    pg.event.post(event_blackout)
                    self.blackoutEventSent = True
            case constants.T_STATE_FADING_OUT:
                if self.t_alpha < 255:
                    self.t_alpha += 10
                    if(self.t_alpha > 255):
                        self.t_alpha = 255
                    self.surface.fill((0, 0, 0, self.t_alpha))
                elif self.t_alpha == 255:
                    self.state = constants.T_STATE_BLACKOUT
            case constants.T_STATE_FADING_IN:
                if self.t_alpha > 0:
                    self.t_alpha -= 10
                    if(self.t_alpha < 0):
                        self.t_alpha = 0
                    self.surface.fill((0, 0, 0, self.t_alpha))
                elif self.t_alpha == 0:
                    self.state = constants.T_STATE_IDLE

        return self.surface