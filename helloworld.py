#my first python APP

#just write text in terminal, play sample and open external attached image


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


# image code
pygame.init()

# Cesta k obrázku
image_path = "ascii.png"
if not os.path.exists(image_path):
    print(f"Obrázek '{image_path}' nebyl nalezen.")
    sys.exit(1)

# PŘED convert_alpha() vytvoř okno (video mód)
# Nejprve načti velikost obrázku
temp_img = pygame.image.load(image_path)
img_width, img_height = temp_img.get_size()

# Teď nastav okno
screen = pygame.display.set_mode((img_width, img_height))
pygame.display.set_caption("Vlnící se obrázek")

# A teprve teď použij convert_alpha() – funguje až po set_mode
original_img = temp_img.convert_alpha()


clock = pygame.time.Clock()

# Funkce pro vytvoření vlnícího efektu
def wave_effect(img, t):
    wave_surface = pygame.Surface((img_width, img_height), pygame.SRCALPHA)

    for y in range(img_height):
        # Výpočet posunu pro daný řádek
        offset = int(math.sin(y * 0.05 + t) * 10)  # amplitude 10px, frekvence 0.05
        wave_surface.blit(img, (offset, y), area=pygame.Rect(0, y, img_width, 1))

    return wave_surface

# Smyčka
running = True
start_time = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = time.time() - start_time

    # Vlnící se obrázek
    distorted_img = wave_effect(original_img, t * 5)  # zrychli čas

    # Vykreslení
    screen.fill((0, 0, 0))
    screen.blit(distorted_img, (0, 0))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()


