from morse.builder import *
from math import pi

# Player controlled mouse
mouse=ATRV()
mouse.properties(Object = True, Graspable = False, Label = "MOUSE")
mouse.translate(x=1.0, z=0.2)
mouse.rotate(z=pi)

motion = MotionVW()
motion.add_stream('socket')
mouse.append(motion)

sick = Sick()
sick.properties(laser_range=10,resolution = 30,scan_window = 180,Visible_arc=True)
sick.add_stream('socket')
mouse.append(sick)

keyboard = Keyboard()
keyboard.properties(Speed=5.0)
mouse.append(keyboard)

mpose = Pose()
mpose.add_stream('socket')
mouse.append(mpose)


# Chaser
chaser = Quadrotor()
chaser.translate(x=-7.0, z=1.0)
chaser.rotate(z=pi/3)

'''
semanticF = SemanticCamera()
semanticF.translate(x=0.3, z=-0.08)
semanticF.rotate(y=-pi/6)
semanticF.properties(Vertical_Flip=False)
semanticF.add_stream('socket')
chaser.append(semanticF)
'''

semanticB = SemanticCamera()
semanticB.translate(z=-0.08)
semanticB.rotate(y=-2*pi/5)
semanticB.properties(Vertical_Flip=False)
semanticB.add_stream('socket')
chaser.append(semanticB)

semanticL = SemanticCamera()
semanticL.translate(y=0.1, z=-0.08)
semanticL.rotate(x=+pi/6,y=-pi/6)
semanticL.properties(Vertical_Flip=False)
semanticL.add_stream('socket')
chaser.append(semanticL)

semanticR = SemanticCamera()
semanticR.translate(y=-0.1, z=-0.08)
semanticR.rotate(x=-pi/6,y=-pi/6)
semanticR.properties(Vertical_Flip=False)
semanticR.add_stream('socket')
chaser.append(semanticR)

light = Light()
light.properties(color="(255,0,0)",energy=2.0)
light.rotate(y=2*pi/5)
chaser.append(light);

waypoint = RotorcraftWaypoint()
chaser.append(waypoint)
waypoint.properties(Target="PinkBox")
waypoint.add_stream('socket')

pose = Pose()
chaser.append(pose)
pose.add_stream('socket')


#environment
#env = Environment('land-1/trees')
#env.place_camera([10.0, -10.0, 10.0])
#env.aim_camera([1.0470, 0, 0.7854])
env = Environment('./indoor-1.blend', fastmode = False)
env.place_camera([10.0, -10.0, 10.0])
env.aim_camera([1.05, 0, 0.78])

env.select_display_camera(semanticB)
