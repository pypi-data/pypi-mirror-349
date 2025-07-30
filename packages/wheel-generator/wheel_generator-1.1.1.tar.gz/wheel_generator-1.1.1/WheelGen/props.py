import bpy

class WHEELGEN_Props(bpy.types.PropertyGroup):
    rim_radius: bpy.props.FloatProperty(name="Rim Radius", default=0.5)
    rim_width: bpy.props.FloatProperty(name="Rim Width", default=0.2)
    tire_thickness: bpy.props.FloatProperty(name="Tire Thickness", default=0.1)
    spoke_count: bpy.props.IntProperty(name="Spoke Count", default=6, min=1, max=100)
    apply_materials: bpy.props.BoolProperty(name="Apply Materials", default=True)

    gear_radius: bpy.props.FloatProperty(name="Gear Radius", default=0.6)
    gear_teeth: bpy.props.IntProperty(name="Teeth Count", default=12, min=3, max=100)
    gear_thickness: bpy.props.FloatProperty(name="Gear Thickness", default=0.1)
    gear_rotation: bpy.props.FloatProperty(name="Gear Rotation Angle", default=0.0, description="Rotate gear around Z-axis (degrees)")
