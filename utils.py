import bpy
from random import randint, uniform, choice

def move3DCursor(factor=1, displace=0):
    bpy.context.scene.cursor.location = (
            uniform((0.1*factor)+displace,(30*factor)+displace),
            uniform((0.1*factor)+displace,(30*factor)+displace),
            uniform((0.1*factor)+displace,(30*factor)+displace)
        )

def worldColor(color):
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = color

def changeRenderConfig():
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.samples = randint(1,4)
    bpy.context.scene.cycles.preview_samples = 1
    bpy.context.scene.render.use_motion_blur = True
    bpy.context.scene.render.motion_blur_shutter = uniform(.7, 1)
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.frame_current = randint(1,250)

def createCamera(mesh_nameList):
    bpy.context.scene.cursor.location = (0, 200, 200)
    bpy.ops.object.camera_add()

    bpy.context.scene.camera = bpy.context.active_object
    track_to = bpy.ops.object.constraint_add(type="TRACK_TO")
    camera = bpy.context.active_object
    camera.constraints['Track To'].influence = 0.75
    camera.constraints['Track To'].target = bpy.data.objects[choice(mesh_nameList)]
    bpy.context.scene.frame_set(0)
    return camera
