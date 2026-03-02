import os


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 960, 480
DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT = 512, 384
DIS_RATIO = min(WINDOW_WIDTH / DISPLAY_WIDTH, WINDOW_HEIGHT / DISPLAY_HEIGHT)
MOUSE_VISIBLE = False
FULL_SCREEN = False
TILE_SIZE = 16
FPS = 60

current_dir = os.getcwd()
PATHS = {
    "tilesets": current_dir + "/assets/tilesets",
    "levels": current_dir + "/assets/levels",
    "fonts": current_dir + "/assets/fonts",
    "buttons": current_dir + "/assets/buttons",
    "cursors": current_dir + "/assets/cursor",
    "objects": current_dir + "/assets/objects",
    "spawns": current_dir + "/assets/spawns",
}
