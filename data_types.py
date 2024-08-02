from settings import *

class Segment:
    def __init__(self,p0: tuple[float], p1: tuple[float], sector_id = None, back_sector_id = None, low_tex_id = None, mid_tex_id = None, up_tex_id = None):
        
        self.pos: tuple[vec2] = vec2(p0), vec2(p1)
        self.vector: vec2 = self.pos[1] - self.pos[0]
        
        self.sector_id: int = sector_id
        self.back_sector_id: int = back_sector_id
        
        self.low_tex_id: int = low_tex_id
        self.mid_tex_id: int = mid_tex_id
        self.up_tex_id: int = up_tex_id
        
        
        self.wall_model_id: set[int] = set()
        
        
class BSPNode:
    def __init__(self):
        self.front:BSPNode = None
        self.back: BSPNode = None
        
        self.splitter_p0: vec2 = None
        self.splitter_p1: vec2 = None
        self.splitter_vec: vec2 = None
        
        self.segment_id: int = None

class Sector:
    def __init__(self, floor_h=None, ceil_h=None, floor_tex_id = None, ceil_tex_id=None):
        
        self.floor_h: float = floor_h
        self.ceil_h: float = ceil_h
        
        self.floor_tex_id: int = floor_tex_id
        self.ceil_tex_id: int = ceil_tex_id
        
        