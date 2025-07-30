import bpy

class WHEELGEN_PT_Panel(bpy.types.Panel):
    bl_label = "Wheel Generator"
    bl_idname = "WHEELGEN_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "WheelGen"

    def draw(self, context):
        layout = self.layout
        props = context.scene.wheel_gen_props

        layout.label(text="Wheel Settings")
        layout.prop(props, "rim_radius")
        layout.prop(props, "rim_width")
        layout.prop(props, "tire_thickness")
        layout.prop(props, "spoke_count")
        layout.prop(props, "apply_materials")
        layout.operator("mesh.generate_wheel", text="Generate Wheel")

        layout.separator()
        layout.label(text="Gear Settings")
        layout.prop(props, "gear_radius")
        layout.prop(props, "gear_teeth")
        layout.prop(props, "gear_thickness")
        layout.prop(props, "gear_rotation")
        layout.operator("mesh.generate_gear", text="Generate Gear")
