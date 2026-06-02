from .car import Car
from .traffic_light import TrafficLight

import pygame as pg
import random
from math import *


class Intersection:
    def __init__(self, cars_per_sec: float):
        self.cars: list[Car] = []

        horiz = 10
        vert = 20
        grace = 1

        self.traffic_lights: list[TrafficLight] = [
            TrafficLight(pg.Rect(50, 350, 100, 100), initial_light="green", red_time=horiz+grace, green_time=vert),
            TrafficLight(pg.Rect(850, 50, 100, 100), initial_light="green", red_time=horiz+grace, green_time=vert),
            TrafficLight(pg.Rect(600, 650, 100, 100), initial_light="red", red_time=vert+grace, green_time=horiz),
            TrafficLight(pg.Rect(300, -150, 100, 100), initial_light="red", red_time=vert+grace, green_time=horiz),
        ]

# (658, 720)
# (349, 69)
# (925, 209)
# (111, 513)
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

            color = "green"
            for traffic_light in self.traffic_lights:
                if traffic_light.area.collidepoint(car.pos):
                    color = traffic_light.current_light

            car.update(dt, color, self.cars)

            if car.reached_destination:
                self.cars.pop(i)

        for traffic_light in self.traffic_lights:
            traffic_light.update(dt)
     
        if spawn_car:
            if car_id == 0:
                self.cars.append(Car(pg.Vector2(-100 - random.randint(0, 1000), 400), [pg.Vector2(800, 400)]))
            if car_id == 1:
                self.cars.append(Car(pg.Vector2(1100 + random.randint(0, 1000), 100), [pg.Vector2(200, 100)], pi))
            if car_id == 2:
                self.cars.append(Car(pg.Vector2(650, 850 + random.randint(0, 1000)), [pg.Vector2(650, -50)], pi/2))
            if car_id == 3:
                self.cars.append(Car(pg.Vector2(350, -350 - random.randint(0, 1000)), [pg.Vector2(350, 550)], -pi/2))

            # if car_id == 4:  # turning cars
            #     self.cars.append(Car(pg.Vector2(-100, 300), [pg.Vector2(500, 300), pg.Vector2(600, 100), pg.Vector2(600, 0)]))
            # if car_id == 5:
            #     self.cars.append(Car(pg.Vector2(1100, 200), [pg.Vector2(500, 200), pg.Vector2(400, 400), pg.Vector2(400, 500)], pi))
            # if car_id == 6:
            #     self.cars.append(Car(pg.Vector2(550, 850), [pg.Vector2(550, 250), pg.Vector2(350, 150), pg.Vector2(250, 150)], pi/2))
            # if car_id == 7:
            #     self.cars.append(Car(pg.Vector2(450, -350), [pg.Vector2(450, 250), pg.Vector2(650, 350), pg.Vector2(750, 350)], -pi/2))

    def draw(self, surf: pg.Surface, camera: pg.Vector2):
        for traffic_light in self.traffic_lights:
            traffic_light.draw(surf, camera)

        for car in self.cars:
            car.draw(surf, camera)

