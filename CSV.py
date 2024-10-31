import pygame
from csv import reader
from os import walk


def import_files(path):
    map_1 = []
    with open(path) as border:
        layout = reader(border, delimiter=',')
        for row in layout:
            map_1.append(list(row))
        return map_1


def import_folder(path):
    img_list = []
    for _, __, items in walk(path):
        for image in items:
            full_path = path + '/' + image
            img_surface = pygame.image.load(full_path).convert_alpha()
            img_list.append(img_surface)
    return img_list
