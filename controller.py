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

def main():
	""" Use the semantic cameras to locate the target and follow it """
	with Morse() as morse:
		semanticL = morse.cat.semanticL
		#semanticR = morse.cat.semanticR
		motion = morse.cat.stabilizedquadrotor

		while True:
			mouse_seen_left = is_mouse_visible(semanticL)
			#mouse_seen_right = is_mouse_visible(semanticR)
			#pitch,roll,yaw,height
			mot = {"theta_c":0,"phi_c":0,"psi_c":0,"h_c":15}
			motion.publish(mot)
			

if __name__ == "__main__":
	main()
