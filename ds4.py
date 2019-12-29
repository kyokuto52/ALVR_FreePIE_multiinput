if starting:
	alvr.two_controllers = True
	alvr.override_controller_position = True
	alvr.override_controller_orientation = True
	alvr.override_head_position = True
	speed = 0.003

#		diagnostics.debug("{0}Down".format(key))
#		diagnostics.debug(alvr.controller_orientation[idvr][idvrkey])


def move(id,key,idvr,idvrkey,var):
	if joystick[id].getDown(key):
		alvr.controller_position[idvr][idvrkey] += var

move(0,0,0,0,-0.001)
move(0,2,0,0,0.001)
move(0,3,0,2,-0.001)
move(0,1,0,2,0.001)

alvr.controller_orientation[0][1] = joystick[0].z / -1000.0
alvr.controller_orientation[0][2] = joystick[0].zRotation / -1000.0

alvr.buttons[0][alvr.Id("grip")] = joystick[0].getDown(5)
alvr.buttons[0][alvr.Id("trigger")] = joystick[0].getDown(7)
alvr.buttons[0][alvr.Id("application_menu")] = joystick[0].getDown(9)


