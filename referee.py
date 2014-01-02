"""
Referee
Shows statistics
"""

import scipy as sp
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
from pymorse import Morse
import math
from pprint import pprint

times = []
dists = []

def outputData():
	avgDist = np.average(dists)
	stdDist = np.std(dists)
	argMin  = np.argmin(dists)
	plt.plot(times,dists)
	print("Average Dist.:")
	print(avgDist)
	print("Stand. Dev.:")
	print(stdDist)
	print("Closest Dist:")
	print(dists[argMin])
	print(times[argMin])
	input("Press Enter to continue...")

import atexit
atexit.register(outputData)

def main():

	with Morse() as morse:
		chaserPose = morse.chaser.pose
		mousePose  = morse.mouse.mpose
		start = time.time()
		
		while True:
			chaserPos = chaserPose.get()
			mousePos  = mousePose.get()
			distX = chaserPos['x']-mousePos['x']
			distY = chaserPos['y']-mousePos['y']
			distZ = chaserPos['z']-mousePos['z']
			dist  = sqrt(distX*distX+distY*distY+distZ*distZ)
			times.append(time.time()-start)
			dists.append(dist)
			

if __name__ == "__main__":
	main()
