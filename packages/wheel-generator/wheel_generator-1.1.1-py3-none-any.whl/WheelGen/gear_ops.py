import bpy
import math

class GenerateGearOperator(bpy.types.Operator):
    bl_idname = "mesh.generate_gear"
    bl_label = "Generate Gear"

    def execute(self, context):
        props = context.scene.wheel_gen_props
        radius = props.gear_radius
        teeth = props.gear_teeth
        thickness = props.gear_thickness
        rotation = props.gear_rotation

        bpy.ops.mesh.primitive_circle_add(vertices=teeth * 2, radius=radius, fill_type='NGON')
        gear = bpy.context.active_object
        gear.name = "GearBase"

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, thickness)})
        bpy.ops.object.mode_set(mode='OBJECT')

        gear.rotation_euler[2] = math.radians(rotation)
        gear.location = (0, 0, 0)

        return {'FINISHED'}
