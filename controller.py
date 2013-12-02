from pymorse import Morse

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
		#semanticR = morse.cat.semanticR
		pose = morse.cat.pose
		motion = morse.cat.waypoint
		
		while True:
			mouse_seen_left = is_mouse_visible(semanticL)
			#mouse_seen_right = is_mouse_visible(semanticR)
			#pitch,roll,yaw,height
			#mot = {"theta_c":0,"phi_c":0,"psi_c":0,"h_c":15}
			#motion.publish(mot)
			pos=where_is(pose)
			waypoint = {	"x": 5, \
								"y": 5, \
								"z": 2, \
								"yaw": 0, \
								"tolerance": 0.5 \
							}
			print(pos)
			#motion.publish(waypoint)
			
			

if __name__ == "__main__":
	main()
