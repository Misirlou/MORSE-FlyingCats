from pymorse import Morse
import math


dist=1.5
height=5

def is_mouse_visible(semantic_camera_stream):
	""" Read data from th	e semantic camera, and determine if a specific
	object is within the field of view of the robot """
	data = semantic_camera_stream.get()
	visible_objects = data['visible_objects']
	for visible_object in visible_objects:
		if visible_object['name'] == "MOUSE":
			return True
	return False
	
def where_is(agentPose_stream):
	pose = agentPose_stream.get()
	return pose
	



def main():
	""" Use the semantic cameras to locate the target and follow it """
	with Morse() as morse:
		semanticL = morse.cat.semanticL
		semanticR = morse.cat.semanticR
		semanticF = morse.cat.semanticF
		pose = morse.cat.pose
		motion = morse.cat.waypoint
		#motion=morse.cat.catmotion
		
		while True:
			mouse_seen_left = is_mouse_visible(semanticL)
			mouse_seen_right = is_mouse_visible(semanticF)
			mouse_seen_front = is_mouse_visible(semanticR)
			#mouse_seen_right = is_mouse_visible(semanticR)
			#pitch,roll,yaw,height
			#mot = {"theta_c":0,"phi_c":0,"psi_c":0,"h_c":15}
			#motion.publish(mot)
			pos=where_is(pose)
			waypoint={ "x":pos['x']+dist*math.cos(pos['yaw']),"y":pos['y']+dist*math.sin(pos['yaw']),"z":height,"yaw":pos['yaw'],"tolerance":0.5}
			
			if mouse_seen_front:
				waypoint={ "x":pos['x']+dist*math.cos(pos['yaw']),"y":pos['y']+dist*math.sin(pos['yaw']),"z":height,"yaw":pos['yaw'],"tolerance":0.5}
			elif mouse_seen_right:
				rotate=pos['yaw']-math.pi/6
				waypoint={ "x":pos['x']+dist*math.cos(pos['yaw']),"y":pos['y']+dist*math.sin(pos['yaw']),"z":height,"yaw":rotate,"tolerance":0.5}
			elif mouse_seen_left:
				rotate=pos['yaw']+math.pi/6
				waypoint={ "x":pos['x']+dist*math.cos(pos['yaw']),"y":pos['y']+dist*math.sin(pos['yaw']),"z":height,"yaw":rotate,"tolerance":0.5}
			print(pos['yaw'])
			motion.publish(waypoint)
			#motion.publish({"roll":0,"pitch":0.2,"yaw":0.1,"thrust":2})
			

if __name__ == "__main__":
	main()
