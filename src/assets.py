import pygame as pg
import pathlib, json

from .common import ASSETS_DIRECTORY
from .settings import *


images = {}
data = {}

def load_image(path: pathlib.Path):
    if path.name not in images:
        images[path.name] = pg.image.load(path).convert_alpha()

def clip_img(surf, x: int, y: int, width: int, height: int):
    img_copy = surf.copy()
    clip_rect = pg.Rect(x, y, width, height)
    img_copy.set_clip(clip_rect)
    return img_copy.subsurface(img_copy.get_clip())

def load_images_from_dir(path: pathlib.Path):
    images = {}

    path.iterdir()
    image_paths = [i for i in path.iterdir() if i.is_file()]

    for image_path in image_paths:
        load_image(image_path)

def is_transparent(surface: pg.Surface):
    for y in range(0, surface.get_height()):
        for x in range(0, surface.get_width()):
            if surface.get_at((x, y))[3] > 0:
                return False
    return True

def load_tileset_from_dir(path: pathlib.Path):
    data = {}

    with open(str(path / "data.json"), "r") as f:
        data = json.load(f)

    tileset = {}
    tileset_image = pg.image.load(path / "spritesheet.png").convert_alpha()
    for y in range(0, tileset_image.get_height(), TILE_SIZE):
        for x in range(0, tileset_image.get_width(), TILE_SIZE):
            img = clip_img(tileset_image, x, y, TILE_SIZE, TILE_SIZE)
            if not is_transparent(img):
                tileset[y//TILE_SIZE * tileset_image.get_width()//TILE_SIZE + x//TILE_SIZE] = img

    data.update({data["id"]: data})
    images.update({data["id"]: tileset})

def load_spritesheet_from_dir(path: pathlib.Path):
    data = {}

    with open(str(path / "data.json"), "r") as f:
        data = json.load(f)

    spritesheet = {}
    spritesheet_image = pg.image.load(path / "spritesheet.png").convert_alpha()
    for sprite_id, sprite in data["sprites"].items():
        outline = sprite["outline"]
        x = outline["x"]
        y = outline["y"]
        w = outline["w"]
        h = outline["h"]
        spritesheet[sprite_id] = clip_img(spritesheet_image, x, y, w, h)

    data.update({data["id"]: data})
    images.update({data["id"]: spritesheet})

def load_assets():
    load_spritesheet_from_dir(ASSETS_DIRECTORY / "props")
    load_spritesheet_from_dir(ASSETS_DIRECTORY / "spawns")
    load_tileset_from_dir(ASSETS_DIRECTORY / "tilesets" / "grass")
    load_image(ASSETS_DIRECTORY / "cursor" / "cursor.png")

