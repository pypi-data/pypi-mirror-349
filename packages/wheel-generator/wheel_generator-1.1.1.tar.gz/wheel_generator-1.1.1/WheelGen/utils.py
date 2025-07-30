import bpy

def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')
