from settings import *
from level_data import LevelData
from map_renderer import MapRenderer
from bsp.bsp_builder import BSPTreeBuilder
from bsp.bsp_traverser import BSPTreetraverser
from camera import Camera

class Engine: 
    def __init__(self, app):
        self.app = app
        
        self.level_data = LevelData(self)
        self.bsp_builder = BSPTreeBuilder(self)
        
        self.camera = Camera(self)
        
        self.bsp_traverser = BSPTreetraverser(self)
        self.map_renderer = MapRenderer(self)
    
    def update(self):
        self.bsp_traverser.update()
    
    def draw_2d(self):
        self.map_renderer.draw()
    
    def draw_3d(self):
        ray.begin_mode_3d(self.camera.m_cam)
        
        ray.draw_grid(32,1.0)
        
        ray.end_mode_3d()
    
    def draw(self):
        ray.begin_drawing()
        ray.clear_background(ray.BLACK)
        self.draw_3d()
        #self.draw_2d()
        
        ray.end_drawing()