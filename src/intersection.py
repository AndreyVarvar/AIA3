from .car import Car
from .traffic_light import TrafficLight

import pygame as pg
import random
from math import *


class Intersection:
    def __init__(self, cars_per_sec: float):
        self.cars: list[Car] = []
        self.traffic_lights: list[TrafficLight] = []
        self.cps = cars_per_sec

        self.time_since_last_spawn = 0

    def update(self, dt: float):
        spawn_car = False
        car_id = 0
        self.time_since_last_spawn += dt
        if self.time_since_last_spawn >= 1/self.cps:
            self.time_since_last_spawn -= 1/self.cps
            spawn_car = True
            car_id = random.randrange(4)

        for i in range(len(self.cars))[::-1]:
            car = self.cars[i]

            car.update(dt, "green", self.cars)

            if car.reached_destination:
                self.cars.pop(i)

        for traffic_light in self.traffic_lights:
            traffic_light.update(dt)
     
        if spawn_car:
            # if car_id == 0:
            #     self.cars.append(Car(pg.Vector2(-100, 300), [pg.Vector2(500, 300), pg.Vector2(600, 100), pg.Vector2(600, 0)]))
            if car_id == 0:
                self.cars.append(Car(pg.Vector2(-100, 400), [pg.Vector2(800, 400)]))
            # if car_id == 2:
            #     self.cars.append(Car(pg.Vector2(1100, 200), [pg.Vector2(500, 200), pg.Vector2(400, 400), pg.Vector2(400, 500)], pi))
            if car_id == 1:
                self.cars.append(Car(pg.Vector2(1100, 100), [pg.Vector2(200, 100)], pi))

            # if car_id == 4:
            #     self.cars.append(Car(pg.Vector2(550, 850), [pg.Vector2(550, 250), pg.Vector2(350, 150), pg.Vector2(250, 150)], pi/2))
            if car_id == 2:
                self.cars.append(Car(pg.Vector2(650, 850), [pg.Vector2(650, -50)], pi/2))
            # if car_id == 6:
            #     self.cars.append(Car(pg.Vector2(450, -350), [pg.Vector2(450, 250), pg.Vector2(650, 350), pg.Vector2(750, 350)], -pi/2))
            if car_id == 3:
                self.cars.append(Car(pg.Vector2(350, -350), [pg.Vector2(350, 550)], -pi/2))

    def draw(self, surf: pg.Surface, camera: pg.Vector2):
        for traffic_light in self.traffic_lights:
            traffic_light.draw(surf, camera)

        for car in self.cars:
            car.draw(surf, camera)

