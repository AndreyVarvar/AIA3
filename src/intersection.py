from .car import Car
from .traffic_light import TrafficLight

import pygame as pg
import random
from math import *


class Intersection:
    def __init__(self, cars_per_sec: float):
        self.cars: list[Car] = []

        self.traffic_lights: list[TrafficLight] = self.init_traffic_lights()

        self.cps = cars_per_sec

        self.data = self.init_data()

        self.runtime = 0

    def init_data(self):
        return {
            "average waiting time": 0.0,
            "longest wait": 0.0,
            "cars seen": 0,
        }

    def poisson(self, dt):
        return random.random() < (1 - exp(-self.cps * dt))

    def init_traffic_lights(self, horizontal: int = 10, vertical: int = 20):
        horiz = horizontal
        vert = vertical
        grace = 3
        
        return [
            TrafficLight(pg.Rect(50, 350, 100, 100), initial_light="green", red_time=horiz+grace, green_time=vert),
            TrafficLight(pg.Rect(850, 50, 100, 100), initial_light="green", red_time=horiz+grace, green_time=vert),
            TrafficLight(pg.Rect(600, 650, 100, 100), initial_light="red", red_time=vert+grace, green_time=horiz, start_time=grace/2),
            TrafficLight(pg.Rect(300, -150, 100, 100), initial_light="red", red_time=vert+grace, green_time=horiz, start_time=grace/2),
        ]

    def update_traffic_light_timing(self, horizontal: int = 10, vertical: int = 20):
        data = self.data.copy()
        self.traffic_lights = self.init_traffic_lights(horizontal, vertical)
        self.data = self.init_data()

        self.runtime = 0.0

        return data  # return a copy of data

    def update(self, dt: float):
        self.runtime += dt

        spawn_car = False
        car_id = 0
        if self.poisson(dt):
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
                self.data["average waiting time"] = (self.data["average waiting time"] * self.data["cars seen"] + car.wait_time) / (self.data["cars seen"] + 1)
                self.data["cars seen"] += 1
                if car.wait_time >= self.data["longest wait"]:
                    self.data["longest wait"] = car.wait_time
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

