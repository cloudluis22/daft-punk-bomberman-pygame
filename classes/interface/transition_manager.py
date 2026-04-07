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
    
    def transition_fade_out(self):
        if self.state == constants.T_STATE_IDLE:
            self.state = constants.T_STATE_FADING_OUT

    def transition_fade_in(self):
        if self.state == constants.T_STATE_BLACKOUT:
            self.state = constants.T_STATE_FADING_IN

    def draw_transition(self):
        match self.state:
            case constants.T_STATE_IDLE:
                self.surface.fill((0, 0, 0, 0))
            case constants.T_STATE_BLACKOUT:
                self.surface.fill((0, 0, 0, 255))
            case constants.T_STATE_FADING_OUT:
                if self.t_alpha < 255:
                    self.t_alpha += 5
                    self.surface.fill((0, 0, 0, self.t_alpha))
                elif self.t_alpha == 255:
                    self.state = constants.T_STATE_BLACKOUT

        return self.surface