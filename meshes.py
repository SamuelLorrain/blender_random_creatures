import bpy
from colors import *
from utils import *
from random import randint, uniform

def createMesh(name, color):
    mesh_name = name
    lattice_name = name + "_lattice"
    # Create mesh
    seed = randint(0,1000)
    z_axis_transform = uniform(0,2)
    y_axis_transform = uniform(0,2)
    x_axis_transform = uniform(0,2)
    cuts = randint(10,100)
    fractal = randint(10,30)

    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode="OBJECT")
    primitive = choice(['cube','ico_sphere', 'cylinder'])
    if primitive == 'cube':
        bpy.ops.mesh.primitive_cube_add()
    elif primitive == 'ico_sphere':
        bpy.ops.mesh.primitive_ico_sphere_add()
    elif primitive == 'cylinder':
        bpy.ops.mesh.primitive_cylinder_add()
    bpy.context.object.name = mesh_name
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.subdivide(number_cuts=cuts, fractal=fractal, seed=seed)

    bpy.ops.transform.resize(
        value=(
            uniform(0,2),
            uniform(0,2),
            uniform(0,2),
        ),
        constraint_axis=(True, True, True)
    )

    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action='DESELECT')

    # Create lattice
    bpy.ops.object.add(type="LATTICE")
    bpy.context.object.name = lattice_name
    bpy.ops.object.mode_set(mode="EDIT")
    lattice_data = bpy.context.active_object.data
    bpy.ops.lattice.select_random(seed=seed + randint(0,100000))
    bpy.ops.transform.resize(value=(z_axis_transform*uniform(-1,2),
                                    x_axis_transform*uniform(1,2),
                                    y_axis_transform*uniform(1,2)))
    bpy.ops.object.mode_set(mode="OBJECT")

    # Modifier & appli modifier
    bpy.ops.object.select_all(action="DESELECT")
    bpy.data.objects[mesh_name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[mesh_name]
    bpy.ops.object.modifier_add(type="LATTICE")
    bpy.context.object.modifiers["Lattice"].object = bpy.data.objects[lattice_name]
    bpy.ops.object.modifier_apply(modifier="Lattice")
    bpy.ops.object.select_all(action="DESELECT")
    bpy.data.objects[lattice_name].select_set(True)
    bpy.ops.object.delete()
    bpy.data.objects[mesh_name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[mesh_name]

    # New Material
    obj = bpy.context.active_object
    mat = bpy.data.materials.new(name="Material_" + mesh_name)
    #if choice([False,False,False,True]):
    mat.use_nodes = True
    mat.node_tree.nodes.new("ShaderNodeBsdfVelvet")
    inp = mat.node_tree.nodes['Material Output'].inputs['Surface']
    outp = mat.node_tree.nodes['Velvet BSDF'].outputs['BSDF']
    mat.node_tree.nodes['Velvet BSDF'].inputs[0].default_value = color
    mat.node_tree.nodes['Velvet BSDF'].inputs[1].default_value = uniform(50,100)
    mat.node_tree.links.new(inp,outp)
    mat.diffuse_color = color
    obj.active_material = mat
    #else:
    #    mat.diffuse_color = color
    #    obj.data.materials.append(mat)

def randomMoveCurrentMesh(factor=1):
    x = uniform(-50*factor,50*factor)
    y = uniform(-50*factor,50*factor)
    z = uniform(-50*factor,50*factor)
    axis = choice(['x','y','z'])
    if axis == 'x':
        bpy.ops.transform.translate(value=(x,0,0))
    elif axis == 'y':
        bpy.ops.transform.translate(value=(0,y,0))
    else:
        bpy.ops.transform.translate(value=(0,0,z))

def randomRotateCurrentMesh(factor=1):
    bpy.ops.transform.rotate(value=uniform(-5*factor,5*factor), orient_axis=choice(['X','Y','Z']))

def createLightPlane(mat_name="Light", rotX=0, rotY=0, rotZ=0):
    move3DCursor(3,10)
    bpy.context.scene.cursor.location = (0, -300, 200)
    bpy.ops.mesh.primitive_plane_add(size=200, rotation=(rotX, rotY, rotZ))
    bpy.ops.transform.rotate(value=2.3, orient_axis='X')
    plane = bpy.context.active_object

    mat = bpy.data.materials.new(mat_name)
    bpy.data.materials[mat_name].use_nodes = True
    bpy.data.materials[mat_name].node_tree.nodes.new(type="ShaderNodeEmission")
    inp = bpy.data.materials[mat_name].node_tree.nodes['Material Output'].inputs['Surface']
    outp = bpy.data.materials[mat_name].node_tree.nodes['Emission'].outputs['Emission']
    bpy.data.materials[mat_name].node_tree.nodes['Emission'].inputs[1].default_value = 10
    bpy.data.materials[mat_name].node_tree.links.new(inp,outp)
    plane.active_material = bpy.data.materials[mat_name]
    return plane
