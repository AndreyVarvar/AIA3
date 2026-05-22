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
    # Car(pg.Vector2(100, 200), [pg.Vector2(600, 200)]),
    # Car(pg.Vector2(100, 500), [pg.Vector2(600, 500)]),
    # Car(pg.Vector2(400, 500), [pg.Vector2(400, 100)], rotation=pi/2),
]


camera = pg.Vector2(0, -100)

clock = pg.time.Clock()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    dt = clock.tick(60) / 1_000
    keys_pressed = pg.key.get_pressed()
    keys_just_pressed = pg.key.get_just_pressed()

    for i in range(len(cars))[::-1]:
        car = cars[i]

        car.update(dt, ["green", "red"][not keys_pressed[pg.K_r]], cars)
        if car.reached_destination:
            cars.pop(i)

    display.fill((0, 0, 0))

    for car in cars:
        car.draw(display, camera)

    if keys_pressed[pg.K_r]:
        display.blit(text_green, (10, 10))
    else:
        display.blit(text_red, (10, 10))

    if keys_just_pressed[pg.K_1]:
        cars.append(Car(pg.Vector2(-100, 300), [pg.Vector2(500, 300), pg.Vector2(600, 100), pg.Vector2(600, 0)]))
    if keys_just_pressed[pg.K_2]:
        cars.append(Car(pg.Vector2(-100, 400), [pg.Vector2(800, 400)]))
    if keys_just_pressed[pg.K_3]:
        cars.append(Car(pg.Vector2(1100, 200), [pg.Vector2(500, 200), pg.Vector2(400, 400), pg.Vector2(400, 500)], pi))
    if keys_just_pressed[pg.K_4]:
        cars.append(Car(pg.Vector2(1100, 100), [pg.Vector2(200, 100)], pi))

    if keys_just_pressed[pg.K_5]:
        cars.append(Car(pg.Vector2(550, 850), [pg.Vector2(550, 250), pg.Vector2(350, 150), pg.Vector2(250, 150)], pi/2))
    if keys_just_pressed[pg.K_6]:
        cars.append(Car(pg.Vector2(650, 850), [pg.Vector2(650, -50)], pi/2))
    if keys_just_pressed[pg.K_7]:
        cars.append(Car(pg.Vector2(450, -350), [pg.Vector2(450, 250), pg.Vector2(650, 350), pg.Vector2(750, 350)], -pi/2))
    if keys_just_pressed[pg.K_8]:
        cars.append(Car(pg.Vector2(350, -350), [pg.Vector2(350, 550)], -pi/2))

    camera_speed = 500
    if keys_pressed[pg.K_LEFT]:
        camera.x -= camera_speed * dt
    if keys_pressed[pg.K_RIGHT]:
        camera.x += camera_speed * dt
    if keys_pressed[pg.K_UP]:
        camera.y -= camera_speed * dt
    if keys_pressed[pg.K_DOWN]:
        camera.y += camera_speed * dt

    window.flip()



