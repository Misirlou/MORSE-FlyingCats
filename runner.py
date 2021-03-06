"""
Runner AI
Tries to get away from the Quadcopter
"""

from pymorse import Morse
import math
from pprint import pprint

V_FRONT=2
V_BACK=-1
V_ROTATE=1.5
V_FULLROTATE=0
W_LEFT=1
W_RIGHT=-1
RANGE_TH=3

def readSonar(sonar_stream):
	sonar=sonar_stream.get()
	return sonar["range_list"];


class KnowledgeBase:
	def __init__(self,sonar):
		self.sonar=sonar
		self.dir={"v":2,"w":0}
		self.last_wall=0
	def updatePos(self):
		self.sonarArr = readSonar(self.sonar)
	def updateDir(self): # Updates the car position
		self.wallFollower()
		
	def wallFollower(self):
		if self.sonarArr[3]<RANGE_TH:
			self.dir={"v":V_BACK,"w":W_LEFT};
			#self.dir={"v":0,"w":0};
			self.last_wall=W_LEFT
			print("front obstacle");
		elif self.sonarArr[6]<RANGE_TH:
			self.dir={"v":V_ROTATE,"w":W_RIGHT};
			self.last_wall=W_LEFT
			print("left obstacle");
		elif self.sonarArr[0]<RANGE_TH:
			self.dir={"v":V_FULLROTATE,"w":W_LEFT};
			self.last_wall=W_RIGHT
			print("right obstacle");
		else:
			self.dir={"v":2,"w":self.last_wall};
			print("nothing");
	def getDir(self):
		return self.dir


def main():

	with Morse() as morse:
		sonar=morse.mouse.sick
		motion = morse.mouse.motion
		kb = KnowledgeBase(sonar)
		
		while True:
			kb.updatePos()
			kb.updateDir()
			motion.publish(kb.getDir())
			

if __name__ == "__main__":
	main()
