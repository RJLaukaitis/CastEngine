from settings import *
from data_types import *
from levels.test_level import *

class LevelData:
    def __init__(self, engine):
        self.engine = engine
        
        self.raw_segments = [Segment(p0,p1) for (p0,p1) in SEGMENTS]
        self.settings = SETTINGS
        
        self.sector_data = SECTOR_DATA
        self.segments_of_sector_boundaries = SEGMENTS_OF_SECTOR_BOUNDARIES
        
        self.sectors = {}
        self.handle_sector_data()
        
        self.raw_segments = []
        self.handle_segments_of_sector_boundaries()
        
    def handle_sector_data(self):
        for sec_id, sector_data in self.sector_data.items():
            
            sector = Sector(
                floor_h= sector_data['floor_h'],
                ceil_h= sector_data['ceil_h'],
                floor_tex_id=sector_data.get('floor_tex_id', 0),
                ceil_tex_id=sector_data.get('ceil_tex_id', 0),
            )
            self.sectors[sec_id] = sector
    
    def handle_segments_of_sector_boundaries(self):
        for (p0,p1), sector_ids, textures in self.segments_of_sector_boundaries:
            
            seg = self.get_segment(p0, p1, sector_ids, textures)
            self.raw_segments.append(seg)
            
    def get_segment(self, p0, p1, sector_ids, tex_ids):
        seg = Segment(
            p0=p0,
            p1=p1,
            
            sector_id=sector_ids[0],
            back_sector_id=sector_ids[1],
            
            low_tex_id=tex_ids[0],
            mid_tex_id= tex_ids[1],
            up_tex_id=tex_ids[2],
        )
        return seg