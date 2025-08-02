# Python-learning coding

#my first python APP!
#What it does? It combines several audiovideo things mixed together. 
#After run it will write some text in terminal, then play some sound and in the final it opens image with applied effect on it.

#used libraries
import pygame
import os
import math
import time
import sys
import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#text code
print("Image will be viewed immediately after playing sound....😀 so calm down and take it easy my friend.")

#sound code
pygame.mixer.init()
pygame.mixer.music.load("sample.wav")
pygame.mixer.music.play()

#image code
pygame.init()

image_path = "ascii.png"
if not os.path.exists(image_path):
    print(f"Obrázek '{image_path}' nebyl nalezen.")
    sys.exit(1)

#video mode code
temp_img = pygame.image.load(image_path)
img_width, img_height = temp_img.get_size()

#window settings code
screen = pygame.display.set_mode((img_width, img_height))
pygame.display.set_caption("Vlnící se obrázek")

#convert image code
original_img = temp_img.convert_alpha()

clock = pygame.time.Clock()

#image fx code
def wave_effect(img, t):
    wave_surface = pygame.Surface((img_width, img_height), pygame.SRCALPHA)

    for y in range(img_height):
        # Výpočet posunu pro daný řádek
        offset = int(math.sin(y * 0.05 + t) * 10)  # amplitude 10px, frekvence 0.05
        wave_surface.blit(img, (offset, y), area=pygame.Rect(0, y, img_width, 1))

    return wave_surface

#loop code
running = True
start_time = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = time.time() - start_time

    #image fx wave code
    distorted_img = wave_effect(original_img, t * 5)  # zrychli čas

    #image draw code
    screen.fill((0, 0, 0))
    screen.blit(distorted_img, (0, 0))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
