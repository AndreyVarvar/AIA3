import pygame as pg



class TrafficLight:
    def __init__(self, area: pg.Rect, initial_light: str, red_time: float, green_time: float) -> None:
        self.current_light = initial_light
        self.area = area
        self.red_time = red_time
        self.green_time = green_time

        self.time_since_change = 0.0

        self.font = font = pg.font.SysFont("arial", 40)
    
    def update(self, dt):
        self.time_since_change += dt

        if self.current_light == "red":
            if self.time_since_change >= self.red_time:
                self.current_light = "green"
                self.time_since_change -= self.red_time

        elif self.current_light == "green":
            if self.time_since_change >= self.green_time:
                self.current_light = "red"
                self.time_since_change -= self.green_time

    def draw(self, surf: pg.Surface, camera: pg.Vector2):
        light_color = pg.Color(0, 255, 0, 128) if self.current_light == "green" else pg.Color(255, 0, 0, 128)
        image = pg.Surface(self.area.size, pg.SRCALPHA)
        image.fill(light_color)
        pg.draw.rect(image, self.current_light, self.area.move_to(topleft=(0, 0)), 5)

        text = self.font.render(f"{((self.green_time if self.current_light == 'green' else self.red_time)-self.time_since_change):.0f}", True, self.current_light)
        text_rect = text.get_rect(center=self.area.move_to(topleft=(0, 0)).center)
        image.blit(text, text_rect)

        surf.blit(image, self.area.move(-camera))
