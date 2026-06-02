# ideas for simulation:
# 4-way intersection
# simple raod crossing
# 3-way intersection
from __future__ import annotations
import pygame as pg
from src.intersection import Intersection

pg.init()


window = pg.Window("visualiser", size=(800, 800))
display = window.get_surface()
font = pg.sysfont.SysFont("arial", size=20)
text_green = font.render("GREEN", True, (0, 255, 0))
text_red = font.render("RED (press 'R' to change)", True, (255, 0, 0))


camera = pg.Vector2(0, -100)

intersection = Intersection(1)

clock = pg.time.Clock()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    dt = clock.tick(60) / 1_000
    keys_pressed = pg.key.get_pressed()
    keys_just_pressed = pg.key.get_just_pressed()

    intersection.update(dt)

    if keys_just_pressed[pg.K_m]:
        print(pg.mouse.get_pos())

    display.fill((0, 0, 0))

    intersection.draw(display, camera)

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



