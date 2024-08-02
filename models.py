from settings import *
from data_types import *


class Models:
    def __init__(self, engine):
        self.engine = engine
        #
        self.sectors = engine.level_data.sectors
        self.raw_segments = engine.level_data.raw_segments
        self.segments = engine.bsp_builder.segments
        #self.sector_segments = engine.level_data.sector_segments
        #
        self.wall_models: list[ray.Model] = []
        #
        self.wall_id = 0
        self.build_wall_models()

    def build_wall_models(self):
        for seg in self.raw_segments:
            #
            if seg.back_sector_id is None:
                
                #solid wall
                wall = WallModel(self,seg,wall_type='solid')
                self.add_wall_model(wall,seg)
                
            else:
                front_sector = self.sectors[seg.sector_id]
                back_sector = self.sectors[seg.back_sector_id]

                #portal low wall, built depending on floor height difference
                if abs(front_sector.floor_h - back_sector.floor_h) > EPS:
                    wall = WallModel(self, seg, wall_type='portal_low')
                    self.add_wall_model(wall, seg)
                
                #portal upper wall, built depending on ceiling height difference
                if abs(front_sector.ceil_h - back_sector.ceil_h) > EPS:
                    wall = WallModel(self, seg, wall_type='portal_up')
                    self.add_wall_model(wall,seg)
                
                #portal middle wall, only built if texture is set
                if seg.mid_tex_id is None:
                    wall = WallModel(self,seg,wall_type='portal_mid')
                    self.add_wall_model(wall,seg)                

    def add_wall_model(self, wall_model, segment):
        self.wall_models.append(wall_model)
        #
        segment.wall_model_id.add(self.wall_id)
        self.wall_id += 1


class WallModel:
    def __init__(self, models,segment, wall_type='solid'):
        self.engine = models.engine
        self.segment = segment
        self.sectors = self.engine.level_data.sectors
        self.wall_type = wall_type
        
        #
        self.model: ray.Model = self.get_model()

    def get_model(self):
        mesh = self.get_quad_mesh()
        model = ray.load_model_from_mesh(mesh)
        model.materials[0].maps[ray.MATERIAL_MAP_DIFFUSE].texture = self.get_texture()
        #
        return model

    def get_quad_mesh(self) -> ray.Mesh:
        triangle_count = 2
        vertex_count = 4

        # get seg coords
        (x0, z0), (x1, z1) = self.segment.pos

        # get normals
        delta = vec3(x1, 0, z1) - vec3(x0, 0, z0)
        normal = glm.normalize(vec3(-delta.z, delta.y, delta.x))
        normals = glm.array([normal] * vertex_count)

        # get tex coords
        width = glm.length(delta)
        bottom, top = self.get_wall_height_data()
        #
        uv0, uv1, uv2, uv3 = (0, bottom), (width, bottom), (width, top), (0, top)
        tex_coords = glm.array([glm.vec2(v) for v in [uv0, uv1, uv2, uv3]])

        # get vertices
        v0, v1, v2, v3 = (x0, bottom, z0), (x1, bottom, z1), (x1, top, z1), (x0, top, z0)
        vertices = glm.array([vec3(v) for v in [v0, v1, v2, v3]])

        # get indices
        indices = [0, 1, 2, 0, 2, 3]
        indices = glm.array.from_numbers(glm.uint16, *indices)

        # get mesh
        mesh = ray.Mesh()
        #
        mesh.triangleCount = triangle_count
        mesh.vertexCount = vertex_count
        #
        mesh.vertices = ray.ffi.from_buffer("float []", vertices)
        mesh.indices = ray.ffi.from_buffer("unsigned short []", indices)
        mesh.texcoords = ray.ffi.from_buffer("float []", tex_coords)
        mesh.normals = ray.ffi.from_buffer("float []", normals)

        ray.upload_mesh(mesh, False)
        return mesh

    def get_rnd_col(self):
        col = *glm.ivec3(glm.abs(glm.ballRand(1.0) * 255)), 255
        return col

    def get_texture(self):
        image = ray.gen_image_checked(10, 10, 1, 1, self.get_rnd_col(), WHITE_COLOR)
        texture = ray.load_texture_from_image(image)
        ray.unload_image(image)
        #
        return texture
    
    def get_wall_height_data(self):
        front_sector = self.sectors[self.segment.sector_id]
        
        if self.wall_type == 'solid':
            bottom, top = front_sector.floor_h, front_sector.ceil_h
            return bottom, top

        back_sector = self.sectors[self.segment.back_sector_id]
        
        if self.wall_type =='portal_low':
            bottom, top = front_sector.floor_h, back_sector.floor_h
        
        elif self.wall_type=='portal_up':
            bottom, top = front_sector.ceil_h, back_sector.ceil_h
        
        elif self.wall_type == 'portal_mid':
            bottom, top = (
                max(front_sector.floor_h, back_sector.floor_h),
                min(front_sector.ceil_h, back_sector.ceil_h),
            )
        
        bottom, top = min(bottom, top), max(top,bottom)
        return bottom, top
