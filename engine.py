from settings import *

class Engine: 
    def __init__(self, app):
        self.pp = app
    
    def update(self):
        pass
    
    def draw_2d(self):
        pass
    
    def draw_3d(self):
        pass
    
    def draw(self):
        ray.begin_drawing()
        ray.clear_background(ray.BLACK)
        self.draw_3d()
        self.draw_2d()
        
        ray.end_drawing()