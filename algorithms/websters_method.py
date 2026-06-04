from .algorithm import Algorithm
from src.intersection import Intersection

class WebstersMethod(Algorithm):
    def __init__(self, intersection: Intersection):
        super().__init__(intersection)
        # websters algorithm analizes the intersection information
        # once, and produces the most optimal cycle to use in 
        # general 
        
        n = 4
        lost_time = 2
        all_red_time = 0
        L = (n * lost_time) + all_red_time

        max_vehicle_flow = 4
        y = self.intersection.cps / max_vehicle_flow  # cars per second

        Co = (1.5 * L + 5) / (1 - y)

        # green time of horizontal lanes
        phases = self.intersection.directional_chances
        yh = phases[0] + phases[3]
        Gh = (yh / y) * (Co - L)
        # green time of vertical lanes
        yv = phases[1] + phases[2]
        Gv = (yv / y) * (Co - L)

        self.intersection.update_traffic_light_timing(Gv, Gh)


