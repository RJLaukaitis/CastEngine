from settings import *

class Camera:
    def __init__ (self, engine):
        self.app = engine.app
        self.engine = engine
        
        self.fake_up = vec3(0.0,1.0,0.0)
        
        self.m_cam: ray.Camera3D = self.get_camera()
        
        self.target = self.m_cam.target
        
        self.pos_3d = self.m_cam.position
        self.pos_2d = vec2(self.pos_3d.x, self.pos_3d.z)
        
    def get_camera(self):
        cam = ray.Camera3D(
            self.engine.level_data.settings['cam_pos'],
            self.engine.level_data.settings['cam_target'],
            self.fake_up.to_tuple(),
            FOV_Y_DEG,
            ray.CAMERA_PERSPECTIVE
        )
        return cam
        