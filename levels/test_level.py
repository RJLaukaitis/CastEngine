from settings import *


# points
P_00 = (0.0, 0.0)
P_01 = (7.0, 0.0)
P_02 = (12.0, 0.0)
P_03 = (12.0, 6.0)
#
P_04 = (7.0, 6.0)
P_05 = (0.0, 6.0)

SECTOR_DATA = {
    0: dict(floor_h=0.0, ceil_h=3.0),
    1: dict(floor_h=0.5, ceil_h=3.0),
}


SETTINGS = {
    'seed': 4178,
    'cam_pos': (13, CAM_HEIGHT, 13),
    'cam_target': (5, CAM_HEIGHT, 5)
}


SEGMENTS = [

]

SEGMENTS_OF_SECTOR_BOUNDARIES = {
    #seg points(vertices), sector ids(front or back sector), texture ids (low,mid,up)
    
    #sector 0
    [(P_00, P_01), (0, _), (_,_,_)],
    [(P_04, P_05), (0, _), (_,_,_)],
    [(P_05, P_00), (0, _), (_,_,_)],
    
    [(P_01, P_04), (0, 1), (_,_,_)], #segment between both sectors, 0 faces secotr 0 then 1 faces sector 1
    
    [(P_01, P_02), (0, _), (_,_,_)],
    [(P_02, P_03), (0, _), (_,_,_)],
    [(P_03, P_04), (0, _), (_,_,_)],
}
