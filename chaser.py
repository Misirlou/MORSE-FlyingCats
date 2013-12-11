"""
Chaser AI
Tries to chase the car and land on top of it
"""

from pymorse import Morse
import math

NEAR_DIST     = 1.5  # Landing Distance
SAFETY_HEIGHT = 5    # Safety Height (Stays at this height until its near the car)
CAR_HEIGHT    = 1    # Height of the car
WP_TOLERANCE  = 1    # Waypoint Tolerance

def isCarVisible(semantic_camera_stream):
	""" Read data from the semantic camera, and determine if a specific
	object is within the field of view of the robot """
	data = semantic_camera_stream.get()
	visible_objects = data['visible_objects']
	for visible_object in visible_objects:
		if visible_object['name'] == "MOUSE":
			return {"x":visible_object['position'][0],"y":visible_object['position'][1],"z":visible_object['position'][2]}
	return False
	
def whereIs(agentPose_stream):
	""" Returns the position of an agent based on its pose """
	pose = agentPose_stream.get()
	return pose

class KnowledgeBase:
	def __init__(self,pose):
		self.pos       = whereIs(pose)
		self.goal      = {"x":self.pos['x'],"y":self.pos['y'],"z":SAFETY_HEIGHT,"yaw":self.pos['yaw']}
	def updatePos(self,pose):
		self.pos = whereIs(pose)
	def updateCarPos(self,semanticL,semanticF,semanticR): # Updates the car position
		carSeenLeft  = isCarVisible(semanticL)
		carSeenFront = isCarVisible(semanticF)
		carSeenRight = isCarVisible(semanticR)
		if carSeenFront:
			self.goal["x"]   = carSeenFront["x"];
			self.goal["y"]   = carSeenFront["y"];
			self.goal["z"]   = carSeenFront["z"]+CAR_HEIGHT;
			self.goal["yaw"] = self.pos["yaw"]
		elif carSeenLeft:
			self.goal["x"]   = carSeenLeft["x"];
			self.goal["y"]   = carSeenLeft["y"];
			self.goal["z"]   = carSeenLeft["z"]+CAR_HEIGHT;
			self.goal["yaw"] = self.pos["yaw"]-math.pi/3
		elif carSeenRight:
			self.goal["x"]   = carSeenRight["x"];
			self.goal["y"]   = carSeenRight["y"];
			self.goal["z"]   = carSeenRight["z"]+CAR_HEIGHT;
			self.goal["yaw"] = self.pos["yaw"]+math.pi/3
	def getWaypoint(self):
		dist = math.sqrt((self.goal["x"]-self.pos["x"])**2+(self.goal["y"]-self.pos["y"])**2)
		waypoint = {
			"x":self.goal["x"],
			"y":self.goal["y"],
			"z":self.goal["z"],
			"yaw":self.goal["yaw"],
			"tolerance":WP_TOLERANCE
			}
		if dist>NEAR_DIST:
			waypoint["z"]=SAFETY_HEIGHT
		return waypoint


def main():
	""" Use the semantic cameras to locate the target and follow it """
	with Morse() as morse:
		semanticL = morse.chaser.semanticL
		semanticR = morse.chaser.semanticR
		semanticF = morse.chaser.semanticF
		pose = morse.chaser.pose
		motion = morse.chaser.waypoint
		kb = KnowledgeBase(pose)
		
		while True:
			kb.updatePos(pose)
			kb.updateCarPos(semanticL,semanticF,semanticR);
			motion.publish(kb.getWaypoint())
			

if __name__ == "__main__":
	main()
