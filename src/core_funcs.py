import pygame as pg
import json

from .common import *
from .settings import *

def clip_img(surf, x: int, y: int, width: int, height: int):
    img_copy = surf.copy()
    clip_rect = pg.Rect(x, y, width, height)
    img_copy.set_clip(clip_rect)
    return img_copy.subsurface(img_copy.get_clip())

def get_file_names(dir_path: str):
    files = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            files.append(path.split("/")[-1])
    return files

def get_dir_names(dir_path: str):
    files = []
    for path in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, path)):
            files.append(path)
    return files

def load_images_from_dir(path: str):
    img_names = get_file_names(path)
    images = {}

    for name in img_names:
        img = pg.image.load(os.path.join(path, name)).convert_alpha()
        img.set_colorkey((0, 0, 0))
        images[name.split(".")[0]] = img

    return images

def make_tileset_dict(tileset_path: str):
    tileset = {}
    tileset_img = pg.image.load(tileset_path).convert_alpha()
    for y in range(0, tileset_img.get_height(), TILE_SIZE):
        for x in range(0, tileset_img.get_width(), TILE_SIZE):
            img = clip_img(tileset_img, x, y, TILE_SIZE, TILE_SIZE)

            if not is_transparent(img):
                tileset[y//TILE_SIZE * tileset_img.get_width()//TILE_SIZE + x//TILE_SIZE] = img

    return tileset

def is_transparent(surface: pg.Surface):
    for y in range(0, surface.get_height()):
        for x in range(0, surface.get_width()):
            if surface.get_at((x, y))[3] > 0:
                return False
    return True
