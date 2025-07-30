import bpy
import math
from mathutils import Vector
from .materials import create_rim_material, create_tire_material
from .utils import deselect_all

class GenerateWheelOperator(bpy.types.Operator):
    bl_idname = "mesh.generate_wheel"
    bl_label = "Generate Wheel"

    def execute(self, context):
        props = context.scene.wheel_gen_props

        rim = self.create_rim(props.rim_radius, props.rim_width)
        tire = self.create_tire(props.rim_radius + props.tire_thickness, props.rim_width + 0.05)
        spokes = self.create_spokes(props.rim_radius, props.tire_thickness, props.spoke_count)

        all_parts = [rim, tire] + spokes

        if props.apply_materials:
            metal_mat = create_rim_material()
            rim.data.materials.append(metal_mat)
            for spoke in spokes:
                spoke.data.materials.append(metal_mat)
            tire.data.materials.append(create_tire_material())

        deselect_all()
        for obj in all_parts:
            obj.select_set(True)

        context.view_layer.objects.active = rim
        bpy.ops.object.join()
        bpy.context.active_object.location = (0, 0, 0)

        return {'FINISHED'}

    def create_rim(self, radius, width):
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=radius, depth=width)
        rim = bpy.context.active_object
        rim.name = "Rim"
        return rim

    def create_tire(self, radius, width):
        bpy.ops.mesh.primitive_torus_add(major_radius=radius, minor_radius=0.05, major_segments=64)
        tire = bpy.context.active_object
        tire.name = "Tire"
        tire.scale = (1, 1, width / 0.1)
        return tire

    def create_spokes(self, rim_radius, tire_thickness, count):
        spokes = []
        inner_tire_radius = rim_radius + tire_thickness - 0.05
        spoke_length = inner_tire_radius - rim_radius

        for i in range(count):
            angle = math.radians((360 / count) * i)
            bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=spoke_length)
            spoke = bpy.context.active_object
            spoke.name = f"Spoke_{i}"
            spoke.rotation_euler[1] = math.radians(90)
            spoke.rotation_euler[2] = angle
            spoke.location = Vector((
                (rim_radius + spoke_length / 2) * math.cos(angle),
                (rim_radius + spoke_length / 2) * math.sin(angle),
                0
            ))
            spokes.append(spoke)
        return spokes
