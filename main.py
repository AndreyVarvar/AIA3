# ideas for simulation:
# 4-way intersection
# simple raod crossing
# 3-way intersection
from __future__ import annotations
import pygame as pg
from math import pi
from src.car import Car

pg.init()


window = pg.Window("visualiser", size=(1000, 800))
display = window.get_surface()
font = pg.sysfont.SysFont("arial", size=20)
text_green = font.render("GREEN", True, (0, 255, 0))
text_red = font.render("RED (press 'R' to change)", True, (255, 0, 0))


cars = [
    Car(pg.Vector2(100, 100), [pg.Vector2(600, 100), pg.Vector2(800, 300)]),
    Car(pg.Vector2(100, 200), [pg.Vector2(600, 200)]),
    Car(pg.Vector2(100, 500), [pg.Vector2(600, 500)]),
    Car(pg.Vector2(400, 500), [pg.Vector2(400, 100)], rotation=pi/2),
]



clock = pg.time.Clock()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    dt = clock.tick(60) / 1_000
    keys_pressed = pg.key.get_pressed()

    for i in range(len(cars))[::-1]:
        car = cars[i]

        car.update(dt, ["green", "red"][not keys_pressed[pg.K_r]], cars)
        if car.reached_destination:
            cars.pop(i)

    display.fill((0, 0, 0))

    for car in cars:
        car.draw(display)

    if keys_pressed[pg.K_r]:
        display.blit(text_green, (10, 10))
    else:
        display.blit(text_red, (10, 10))

    window.flip()



