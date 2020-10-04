import bpy
from random import randint, sample
import sys

sys.path.append("/home/samuel/Documents/Prog/Python/blender_random_creatures")

from colors import *
from meshes import *
from animations import *
from utils import *

if __name__ == '__main__':
    savedCursorLocation = bpy.context.scene.cursor.location
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    NUMBER_OF_OBJECTS = randint(6,21)

    rgbColorTheme = [ rgbToBlender(i) for i
                      in generateColorSchemeRgb(
                          generateRandomRgbFromHsv(maxS=0.7),
                          NUMBER_OF_OBJECTS + 1,
                          method="gold"
                      ) ]

    mesh_nameList = []
    for i in range(0,NUMBER_OF_OBJECTS):
        move3DCursor()
        createMesh("mesh_" + str(i), rgbColorTheme[i])
        mesh_nameList.append("mesh_" + str(i))

        randomMoveCurrentMesh()

        # Animate
        for j in sample(range(1, 250), randint(5,50)):
            bpy.context.scene.frame_set(j)
            randomMoveCurrentMesh()
            randomRotateCurrentMesh()
            bpy.ops.anim.keyframe_insert_menu(type="LocRotScale")
            fcurves = bpy.context.active_object.animation_data.action.fcurves
            noiseFCurves(fcurves)

        bpy.context.scene.frame_set(0)

    camera = createCamera(mesh_nameList)

    #Restore cursor location
    bpy.context.scene.cursor.location = savedCursorLocation

    plane = createLightPlane()

    #duplicate plane
    #put it behind camera

    worldColor(rgbColorTheme[NUMBER_OF_OBJECTS])

    changeRenderConfig()
