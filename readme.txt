This is a simulation of a quadrocopter and a car robots using MORSE simulator.

Diogo Basto & João Costa
Robótica - MIEIC - FEUP

OS: Linux with Python 3, Blender and Morse 1.1, see http://www.openrobots.org/morse/doc/stable/user/installation.html for instructions on how to install Morse. 

Sources:
	scene.py : code to establish to load the scene, insert the robots, sensors and actuators
	chaser.py : this source establishes the behaviour of the quadrocopter robot
	runner.py : this source establishes the behaviour of the car robot
	
	
Running:
	-Open a terminal inside this directory and type "morse run scene.py". This will initiate blender and load the scene. The scene can be panned with the WASD keys or orbited with CTRL+mouse move. The car robot can be controlled with the arrow keys.
	-To have the car be automatically controlled, open another terminal and type "python3 runner.py".
	-To run the quadrocopter, open another terminal and type "python3 chaser.py".
	
