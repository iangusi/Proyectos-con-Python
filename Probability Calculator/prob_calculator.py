import copy
import random

# *args  ->  Varios parametros
# **kwargs  ->  Varios params en diccionario
class Hat:
    def __init__(self, **kwargs):
        self.contents = [f"{key}" for key, value in kwargs.items()
            for amount in range(value)]
    def __str__(self):
        return ', '.join(self.contents)
    def draw(self,number=0):
        drawn = []
        if number >= len(self.contents):
            drawn = self.contents.copy()
            self.contents.clear()
        else:
            drawn = random.choices(self.contents,k=number)
            for ball in drawn:
                try:
                    self.contents.remove(ball)
                except:
                    pass
        return drawn

def experiment(hat, expected_balls={}, num_balls_drawn=0, num_experiments=0):
    succes = 0
    for _ in range(num_experiments):
        _hat = copy.deepcopy(hat)
        balls_drawn = _hat.draw(num_balls_drawn)
        all_good = True
        for key,value in expected_balls.items():
            for ball_draw in balls_drawn:
                if ball_draw == key:
                    value -= 1
            if value > 0:
                all_good = False
        if all_good:
            succes += 1
    return succes/num_experiments
