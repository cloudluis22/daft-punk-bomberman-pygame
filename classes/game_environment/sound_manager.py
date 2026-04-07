import pygame as pg
from pathlib import Path

current_path = Path(__file__).parent
root_path = current_path.parent.parent

music_paths_dict = {
    "mus_menu": root_path / "assets" / "sound" / "music" / "music_menu.mp3",
    "mus_level1": root_path / "assets" / "sound" / "music" / "music1.mp3",

}

sfx_paths_dict = {
    "sfx_enemy_hit": root_path / "assets" / "sound" / "sfx" / "enemy_hit.mp3",
    "sfx_player_hit": root_path / "assets" / "sound" / "sfx" / "player_hit.mp3",
    "sfx_explosion": root_path / "assets" / "sound" / "sfx" / "explosion.mp3",
    "sfx_menu_hover": root_path / "assets" / "sound" / "sfx" / "menu-hover.mp3"
}

class SoundManager():
    def __init__(self):

        self.sfx_dict = {}

        self.vol_sfx = 0.7
        self.vol_music = 1
        self.isTrackPlaying = False

        pg.mixer.init()

        for key, path in sfx_paths_dict.items():
            self.sfx_dict[key] = pg.mixer.Sound(path)
            self.sfx_dict[key].set_volume(self.vol_sfx)
        
    def play_sound(self, sound):
        self.sfx_dict[sound].play()

    def play_music(self, track):
        if self.isTrackPlaying == False:
            pg.mixer.music.load(music_paths_dict[track])
            pg.mixer.music.play(-1)
            self.isTrackPlaying = True

