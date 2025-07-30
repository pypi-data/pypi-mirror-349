bl_info = {
    "name": "Wheel Generator",
    "author": "Your Name",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "description": "Generate wheels and gears with rims, tires, and spokes with materials.",
    "category": "Object",
}

import bpy

from .props import WHEELGEN_Props
from .ui_panel import WHEELGEN_PT_Panel
from .wheel_ops import GenerateWheelOperator
from .gear_ops import GenerateGearOperator

classes = [
    WHEELGEN_Props,
    WHEELGEN_PT_Panel,
    GenerateWheelOperator,
    GenerateGearOperator,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.wheel_gen_props = bpy.props.PointerProperty(type=WHEELGEN_Props)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.wheel_gen_props

if __name__ == "__main__":
    register()
