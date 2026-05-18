# ideas for simulation:
# 4-way intersection
# simple raod crossing
# 3-way intersection
from __future__ import annotations
import pygame as pg
from math import sin, cos

pg.init()


window = pg.Window("visualiser", size=(1000, 800))
display = window.get_surface()



class Car:
    def __init__(self, pos: pg.Vector2, destination: pg.Vector2, rotation: float = 0) -> None:
        self.pos = pos
        self.destination = destination

        self.velocity = pg.Vector2(0, 0)
        
        self.acceleration = 0
        self.acceleration_speed = 500
        self.deceleration_speed = -1000

        self.rotation = rotation

        self.image = pg.Surface((100, 50))
        pg.draw.rect(self.image, (255, 255, 255), (0, 0, 100, 50), 2)

        self.speed_limit = 500

    def draw(self, surf: pg.Surface):
        image = pg.transform.rotate(self.image, self.rotation)
        image_rect = image.get_rect(center=self.pos)
        surf.blit(image, image_rect)

        pg.draw.circle(surf, (255, 255, 0), self.destination, 5)

    def update(self, dt: float):
        if self.velocity.magnitude() > self.speed_limit:
            self.acceleration = self.deceleration_speed
        elif abs(self.velocity.magnitude() - self.speed_limit) < 10:
            self.acceleration = 0
        else:
            self.acceleration = self.acceleration_speed


        self.velocity += pg.Vector2(cos(self.rotation), -sin(self.rotation)) * self.acceleration * dt
        self.pos += self.velocity * dt

        if self.pos.x > 1000:
            self.pos.x = 0


cars = [
    Car(pg.Vector2(100, 100), pg.Vector2(600, 100))
]


clock = pg.time.Clock()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    dt = clock.tick(60) / 1_000

    for car in cars:
        car.update(dt)

    display.fill((0, 0, 0))

    for car in cars:
        car.draw(display)

    window.flip()



