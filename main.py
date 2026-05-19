# ideas for simulation:
# 4-way intersection
# simple raod crossing
# 3-way intersection
from __future__ import annotations
import pygame as pg
from math import sin, cos, dist, atan2, pi, degrees

pg.init()


window = pg.Window("visualiser", size=(1000, 800))
display = window.get_surface()



class Car:
    def __init__(self, pos: pg.Vector2, destinations: list[pg.Vector2], rotation: float = 0) -> None:
        self.pos = pos
        self.destinations = destinations

        self.speed = 0

        self.reached_destination = False
        
        self.acceleration = 0
        self.acceleration_speed = 500
        self.deceleration_speed = -2000

        self.rotation = rotation
        self.rotation_speed = 1.5

        self.image = pg.Surface((100, 50), pg.SRCALPHA)
        pg.draw.rect(self.image, (255, 255, 255), (0, 0, 100, 50), 2)

        self.speed_limit = 500

    def draw(self, surf: pg.Surface):
        image = pg.transform.rotate(self.image, degrees(self.rotation))
        image_rect = image.get_rect(center=self.pos)
        surf.blit(image, image_rect)

        for dest in self.destinations:
            pg.draw.circle(surf, (255, 255, 0), dest, 5)

    def update(self, dt: float, signal: str, other_cars: list[Car]):
        # check if we can move
        if signal == "green":
            max_speed = self.speed_limit
        else:
            max_speed = 0


        self.rotation %= 2*pi
        if self.rotation < 0:
            self.rotaion += 2*pi

        # checking if will collide with any cars
        for car in other_cars:
            if car is not self:  
                for r in [0, -pi/8, -pi/4]:
                    for i in range(1, 10):
                        p = self.pos + pg.Vector2(cos(self.rotation + r), -sin(self.rotation + r)) * 10 * i
                        if dist(p, car.pos) < 50:
                            max_speed = 0
                            break
                    if max_speed == 0:
                        break
            if max_speed == 0:
                break
        # check if we reached the speed limit
        if self.speed > max_speed:
            self.acceleration = self.deceleration_speed
        elif abs(self.speed - max_speed) < 10:
            self.acceleration = 0
        else:
            self.acceleration = self.acceleration_speed

        # friction
        self.speed /= 2**dt

        # turning
        destination = self.destinations[0]

        angle = atan2(-destination.y + self.pos.y, destination.x - self.pos.x)
        if angle < 0:
            angle += 2*pi
        if abs(angle - self.rotation) > 0.1:

            diff = (angle - self.rotation) % 2*pi
            print(diff)
            if diff < pi:
                self.rotation += self.rotation_speed * dt * self.speed / self.speed_limit
            else:
                self.rotation -= self.rotation_speed * dt * self.speed / self.speed_limit

        # applying the foces
        self.speed += self.acceleration * dt
        self.pos += pg.Vector2(cos(self.rotation), -sin(self.rotation)) * self.speed * dt

        if dist(self.pos, destination) < 10:
            self.destinations.remove(destination)

        if len(self.destinations) == 0:
            self.reached_destination = True



cars = [
    Car(pg.Vector2(100, 100), [pg.Vector2(600, 100), pg.Vector2(800, 200)]),
    # Car(pg.Vector2(100, 200), [pg.Vector2(600, 200)]),
    # Car(pg.Vector2(100, 500), [pg.Vector2(600, 500)]),
    # Car(pg.Vector2(400, 500), [pg.Vector2(400, 100)], rotation=pi/2),
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

    window.flip()



