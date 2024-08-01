from settings import *
from data_types import BSPNode
from utils import is_on_front


class BSPTreetraverser:
    def __init__(self,engine):
        self.engine = engine
        self.root_node = engine.bsp_builder.root_node
        self.segments = engine.bsp_builder.segments
        
        self.cam_pos = vec2(6,7)
        self.seg_ids_to_draw = []
    
    def update(self):
        self.seg_ids_to_draw.clear()
        self.traverse(self.root_node)
    
    def traverse(self, node: BSPNode):
        if node is None:
            return None
        
        on_front = is_on_front(self.cam_pos - node.splitter_p0, node.splitter_vec)
        
        if on_front:
            self.traverse(node.front)
            
            self.seg_ids_to_draw.append(node.segment_id)
            
            self.traverse(node.back)
        else:
            self.traverse(node.back)
            
            self.traverse(node.front)