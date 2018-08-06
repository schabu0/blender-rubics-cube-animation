import bpy
from bpy import context
from math import radians
from mathutils import Vector
from mathutils import Euler

scene = context.scene
if not scene.sequence_editor:
    scene.sequence_editor_create()

startFrame  = 2  #klatka startowa
frameCount  = 0  #licznik klatek
rotTime     = 30 #czas rotacji
pTime       = 1  #czas pauzy
crTime      = 30 #czas obrotu kamery

   # [  deg,  axis=(x, y, z), loc, axle ] 
L =  [  90.0,       1, 0, 0,  -1,  0    ]
R =  [  90.0,       1, 0, 0,   1,  0    ]
F =  [  90.0,       0, 1, 0,  -1,  1    ]
B =  [  90.0,       0, 1, 0,   1,  1    ]
U =  [  90.0,       0, 0, 1,   1,  2    ]
D =  [  90.0,       0, 0, 1,  -1,  2    ]
L1 = [ -90.0,       1, 0, 0,  -1,  0    ]
R1 = [ -90.0,       1, 0, 0,   1,  0    ]
F1 = [ -90.0,       0, 1, 0,  -1,  1    ]
B1 = [ -90.0,       0, 1, 0,   1,  1    ]
U1 = [ -90.0,       0, 0, 1,   1,  2    ]
D1 = [ -90.0,       0, 0, 1,  -1,  2    ]
l, r, u, d, f, b = [Vector((-19.0, 0.0, 8.0)), Euler((1.1519173383712769, 8.706958709581158e-08, -1.5707967281341553), 'XYZ')], 0, 0, 0, [Vector((0.0, -19.0, 8.0)), Euler((1.1519173383712769, 8.706958709581158e-08, -4.76837158203125e-07), 'XYZ')], 0

mvs = [ U, L, U1, R ]
cam = [ l, l, f , l ]

bpy.context.scene.objects.active = bpy.data.objects["Cube"]

for i in range(0,len(mvs)):
    c = bpy.data.objects['Camera']
    if i == 0:
        bpy.context.scene.frame_set(startFrame+frameCount)
        c.location = cam[i][0]
        c.rotation_euler = cam[i][1]
        c.keyframe_insert(data_path="location")
        c.keyframe_insert(data_path="rotation_euler")
    else:
        if cam[i] != cam[i-1]:
            bpy.context.scene.frame_set(startFrame+frameCount+crTime)
            c.location = cam[i][0]
            c.rotation_euler = cam[i][1]
            c.keyframe_insert(data_path="location")
            c.keyframe_insert(data_path="rotation_euler")
            frameCount += crTime
    bpy.ops.object.select_all(action='DESELECT')
    for ob in bpy.data.groups['cube'].objects:
        print(ob)
        ob.keyframe_insert(data_path="rotation_quaternion")
        if ob.location[mvs[i][5]] > mvs[i][4]:
            print("^^^^^^^")
            ob.select = True
    if mvs[i][4] < 0:
        bpy.ops.object.select_all(action='INVERT')
        print('inverted')
        bpy.data.objects['Camera'].select = False
    print(mvs[i][4])
    bpy.context.scene.frame_set(startFrame+frameCount+rotTime)
    bpy.ops.transform.rotate(value=radians(mvs[i][0]), axis=(mvs[i][1], mvs[i][2], mvs[i][3]))
    for ob in bpy.data.groups['cube'].objects:
        ob.keyframe_insert(data_path="rotation_quaternion")
    c.keyframe_insert(data_path="location")
    c.keyframe_insert(data_path="rotation_euler")
    frameCount += rotTime + pTime

bpy.data.scenes["Scene"].frame_end = frameCount + 2
bpy.ops.object.select_all(action='SELECT')
bpy.data.objects['Camera'].select = False
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.ops.object.select_all(action='DESELECT')
