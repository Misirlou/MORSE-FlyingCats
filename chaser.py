"""
Chaser AI
Tries to chase the car and land on top of it
"""

from pymorse import Morse
import math

NEAR_DIST     = 1.5  # Landing Distance
SAFETY_HEIGHT = 5    # Safety Height (Stays at this height until its near the car)
CAR_HEIGHT    = 0.9    # Height of the car
WP_TOLERANCE  = 0.8    # Waypoint Tolerance
LOST_TH	= 15
LOST_TH_BOTTOM = 10

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
	def __init__(self,pose,semanticL,semanticB,semanticR):
		self.pos       = whereIs(pose)
		self.pose = pose
		self.goal      = {"x":self.pos['x'],"y":self.pos['y'],"z":SAFETY_HEIGHT,"yaw":self.pos['yaw']}
		self.semanticL=semanticL
		self.semanticR=semanticR
		self.semanticB=semanticB
		#self.semanticF=semanticF
		self.lost=0
	def updatePos(self):
		self.pos = whereIs(self.pose)
	def updateCarPos(self): # Updates the car position
		carSeenLeft  = isCarVisible(self.semanticL)
		carSeenFront = isCarVisible(self.semanticB)
		carSeenRight = isCarVisible(self.semanticR)
		
		if carSeenFront:
			self.goal["x"]   = carSeenFront["x"];
			self.goal["y"]   = carSeenFront["y"];
			self.goal["z"]   = carSeenFront["z"]+CAR_HEIGHT;
			self.goal["yaw"] = self.pos["yaw"]
			print("bottom");
			self.lost=LOST_TH_BOTTOM
		elif carSeenLeft and carSeenRight:
			self.goal["x"]   = carSeenLeft["x"];
			self.goal["y"]   = carSeenLeft["y"];
			self.goal["z"]   = carSeenLeft["z"]+CAR_HEIGHT;
			self.goal["yaw"] = self.pos["yaw"]
			print("front");
			self.lost=0
		elif carSeenLeft:
			self.goal["x"]   = carSeenLeft["x"];
			self.goal["y"]   = carSeenLeft["y"];
			self.goal["z"]   = carSeenLeft["z"]+CAR_HEIGHT;
			self.goal["yaw"] = self.pos["yaw"]+math.pi/8
			print("left");
			self.lost=0
		elif carSeenRight:
			self.goal["x"]   = carSeenRight["x"];
			self.goal["y"]   = carSeenRight["y"];
			self.goal["z"]   = carSeenRight["z"]+CAR_HEIGHT;
			self.goal["yaw"] = self.pos["yaw"]-math.pi/8;
			print("right");
			self.lost=0
		else:
			if self.lost<LOST_TH:
				self.lost+=1
			else:
				self.goal["x"]   = self.pos["x"];
				self.goal["y"]   = self.pos["y"];
				self.goal["z"]   = SAFETY_HEIGHT;
				self.goal["yaw"] = self.pos["yaw"]+math.pi/3
				print("lost");
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
		#semanticF = morse.chaser.semanticF
		semanticB = morse.chaser.semanticB
		pose = morse.chaser.pose
		motion = morse.chaser.waypoint
		kb = KnowledgeBase(pose,semanticL,semanticB,semanticR)
		
		while True:
			kb.updatePos()
			kb.updateCarPos();
			motion.publish(kb.getWaypoint())
			

if __name__ == "__main__":
	main()
