from settings import *

class Camera:
    def __init__ (self, engine):
        self.app = engine.app
        self.engine = engine
        
        self.fake_up = vec3(0.0,1.0,0.0)
        
        self.m_cam: ray.Camera3D = self.get_camera()
        
        self.target = self.m_cam.target
        
        self.pos_3d = self.m_cam.position
        self.pos_2d: glm.vec2 = vec2(self.pos_3d.x, self.pos_3d.z)
                
        self.speed = CAM_SPEED
        self.cam_step = vec3(0)
        #
        self.forward = vec3(0)
        self.right = vec3(0)
        
    def get_camera(self):
        cam = ray.Camera3D(
            self.engine.level_data.settings['cam_pos'],
            self.engine.level_data.settings['cam_target'],
            self.fake_up.to_tuple(),
            FOV_Y_DEG,
            ray.CAMERA_PERSPECTIVE
        )
        return cam
    
    def pre_update(self):
        self.init_cam_step()
        self.update_vectors()
    
    def update(self):
        self.check_cam_step()
        self.update_pos_2d()
        self.move()
    
    def update_vectors(self):
        self.forward = self.get_forward()
        self.right = cross(self.forward,self.fake_up)
    
    def get_forward(self) -> glm.vec3:
        return normalize(vec3(
            self.target.x -self.pos_3d.x,
            self.target.y -self.pos_3d.y,
            self.target.z -self.pos_3d.z,
        ))
    
    def init_cam_step(self):
        self.speed = CAM_SPEED * self.app.dt
        self.cam_step *= 0
    
    def step_forward(self):
        self.cam_step += self.speed * self.forward
    
    def step_back(self):
        self.cam_step += -self.speed * self.forward
    
    def step_left(self):
        self.cam_step += -self.speed * self.right
    
    def step_right(self):
        self.cam_step += self.speed * self.right
    
    def check_cam_step(self):
        dx, dz = self.cam_step.xz
        if dx and dz:
            self.cam_step *= CAM_DIAG_MOVE_CORR
    
    def move(self):
        dx, dz = self.cam_step.xz
        self.move_x(dx)
        self.move_z(dz)
    
    def move_x(self, dx):
        self.pos_3d.x += dx
        self.target.x += dx
    
    def move_z(self, dz):
        self.pos_3d.z += dz
        self.target.z += dz
    
    def update_pos_2d(self):
        self.pos_2d[0] = self.pos_3d.x
        self.pos_2d[1] = self.pos_3d.z
        
        
        
    
    
        
        