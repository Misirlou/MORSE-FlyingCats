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

semanticL = SemanticCamera()
semanticL.translate(x=0.3, z=-0.05)
semanticL.rotate(x=+0.2)
semanticL.properties(Vertical_Flip=False)
semanticL.add_stream('socket')
cat.append(semanticL)

stabilizedquadrotor = StabilizedQuadrotor()

# place your component at the correct location
stabilizedquadrotor.translate(0, 0, 0.1)

cat.append(stabilizedquadrotor)

# define one or several communication interface, like 'socket'
stabilizedquadrotor.add_interface('socket')


#environment
env = Environment('land-1/trees')
env.place_camera([10.0, -10.0, 10.0])
env.aim_camera([1.0470, 0, 0.7854])
env.select_display_camera(semanticL)
