from morse.builder import *
from math import pi

#player controlled mouse
mouse=ATRV()
mouse.properties(Object = True, Graspable = False, Label = "MOUSE")
mouse.translate(x=1.0, z=0.2)

keyboard = Keyboard()
keyboard.properties(Speed=3.0)
mouse.append(keyboard)


#flying cat 1

cat = Quadrotor()
cat.translate(x=-7.0, z=1.0)
cat.rotate(z=pi/3)

semanticF = SemanticCamera()
semanticF.translate(x=0.3, z=-0.08)
semanticF.rotate(y=+pi/6)
semanticF.properties(Vertical_Flip=False)
semanticF.add_stream('socket')
cat.append(semanticF)

semanticL = SemanticCamera()
semanticL.translate(y=0.3, z=-0.08)
semanticL.rotate(x=+pi/3,y=+pi/6)
semanticL.properties(Vertical_Flip=False)
semanticL.add_stream('socket')
cat.append(semanticL)

semanticR = SemanticCamera()
semanticR.translate(y=-0.3, z=-0.08)
semanticR.rotate(x=-pi/3,y=+pi/6)
semanticR.properties(Vertical_Flip=False)
semanticR.add_stream('socket')
cat.append(semanticR)

#catmotion = RotorcraftAttitude()
#catmotion.translate(x=0, y=0, z=0.1)
#cat.append(catmotion)
#catmotion.add_stream('socket')

waypoint = RotorcraftWaypoint()
cat.append(waypoint)
waypoint.add_stream('socket')

pose = Pose()
cat.append(pose)
pose.add_stream('socket')


#environment
env = Environment('land-1/trees')
env.place_camera([10.0, -10.0, 10.0])
env.aim_camera([1.0470, 0, 0.7854])

env.select_display_camera(semanticF)
