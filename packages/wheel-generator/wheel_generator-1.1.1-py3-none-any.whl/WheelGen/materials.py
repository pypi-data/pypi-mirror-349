import bpy

def create_rim_material():
    mat = bpy.data.materials.get("RimMaterial")
    if not mat:
        mat = bpy.data.materials.new(name="RimMaterial")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Metallic"].default_value = 1.0
            bsdf.inputs["Roughness"].default_value = 0.3
    return mat

def create_tire_material():
    mat = bpy.data.materials.get("TireMaterial")
    if not mat:
        mat = bpy.data.materials.new(name="TireMaterial")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        for node in nodes:
            nodes.remove(node)

        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (400, 0)

        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        bsdf.inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1)
        bsdf.inputs["Roughness"].default_value = 0.7

        noise = nodes.new(type='ShaderNodeTexNoise')
        noise.location = (-400, 100)
        noise.inputs["Scale"].default_value = 5.0
        noise.inputs["Detail"].default_value = 2.0

        bump = nodes.new(type='ShaderNodeBump')
        bump.location = (-200, 0)
        bump.inputs["Strength"].default_value = 0.3

        links.new(noise.outputs["Fac"], bump.inputs["Height"])
        links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
        links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return mat
