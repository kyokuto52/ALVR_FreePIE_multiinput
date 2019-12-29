if starting:
	xInvert = 1 #set to minus 1 to invert
	yInvert = -1

def avg(list):
	sum = 0
	for item in list:
		sum += item	
	return sum/len(list)

if starting:
	import math
		
	wiimote[0].enable(WiimoteCapabilities.MotionPlus)
	wiimote[1].enable(WiimoteCapabilities.MotionPlus)
	alvr.two_controllers = True
	alvr.override_controller_position = True
	alvr.override_controller_orientation = True
	alvr.override_head_position = True
	
	old_yaw1 = wiimote[0].ahrs.yaw
	old_pitch1 = wiimote[0].ahrs.pitch
	old_roll1 = wiimote[0].ahrs.roll
	
	old_yaw2 = wiimote[1].ahrs.yaw
	old_pitch2 = wiimote[1].ahrs.pitch
	old_roll2 = wiimote[1].ahrs.roll
	
	starting_yaw1, starting_pitch1, starting_roll1 = old_yaw1, old_pitch1, old_roll1
	starting_yaw2, starting_pitch2, starting_roll2 = old_yaw2, old_pitch2, old_roll2	
	
	yaw1 = yaw2 = 0
	pitch1 = pitch2 = 0
	roll1 = roll2 = 0
	
	yaw1_shift = []
	pitch1_shift = []
	roll1_shift = []
	
	yaw2_shift = []
	pitch2_shift = []
	roll2_shift = []

	loop = 0
	
	alvr.controller_orientation[0][0] = 0
	alvr.controller_orientation[0][1] = 0
	alvr.controller_orientation[0][2] = 0
	
	alvr.controller_position[0][0] = 0
	alvr.controller_position[0][1] = 0
	alvr.controller_position[0][2] = 0
	
	alvr.controller_orientation[1][0] = 0
	alvr.controller_orientation[1][1] = 0
	alvr.controller_orientation[1][2] = 0
	
	alvr.controller_position[1][0] = 0
	alvr.controller_position[1][1] = 0
	alvr.controller_position[1][2] = 0
	
	yaw1_blah = pitch1_blah = roll1_blah = yaw2_blah = pitch2_blah = roll2_blah = 0
	scale1 = scale2 = 1
	
if loop < 1000 and wiimote[0].ahrs.yaw != 0 and wiimote[1].ahrs.yaw != 0:
	diagnostics.watch((wiimote[1].ahrs.yaw, wiimote[1].ahrs.pitch, wiimote[1].ahrs.roll))
	diagnostics.watch((wiimote[0].ahrs.yaw, wiimote[0].ahrs.pitch, wiimote[0].ahrs.roll))
	
	loop += 1
	
	yaw1_shift.append(wiimote[0].ahrs.yaw - old_yaw1)
	old_yaw1 = wiimote[0].ahrs.yaw
	
	pitch1_shift.append(wiimote[0].ahrs.pitch - old_pitch1)
	old_pitch1 = wiimote[0].ahrs.pitch
	
	roll1_shift.append(wiimote[0].ahrs.roll - old_roll1)
	old_roll1 = wiimote[0].ahrs.roll
	####
	yaw2_shift.append(wiimote[1].ahrs.yaw - old_yaw2)
	old_yaw2 = wiimote[1].ahrs.yaw
	
	pitch2_shift.append(wiimote[1].ahrs.pitch - old_pitch2)
	old_pitch2 = wiimote[1].ahrs.pitch
	
	roll2_shift.append(wiimote[1].ahrs.roll - old_roll2)
	old_roll2 = wiimote[1].ahrs.roll
	
	
	
if loop == 1000:
	
	yaw1_shift = avg(yaw1_shift[950:])
	pitch1_shift = avg(pitch1_shift[950:])
	roll1_shift = avg(roll1_shift[950:])
	##
	yaw2_shift = avg(yaw2_shift[950:])
	pitch2_shift = avg(pitch2_shift[950:])
	roll2_shift = avg(roll2_shift[950:])

if loop >= 1000:
	loop += 1
	diagnostics.watch("works")
	diagnostics.watch((wiimote[1].ahrs.yaw, wiimote[1].ahrs.pitch, wiimote[1].ahrs.roll))
	diagnostics.watch((wiimote[0].ahrs.yaw, wiimote[0].ahrs.pitch, wiimote[0].ahrs.roll))
	
	yaw1_rad = xInvert * (((wiimote[0].ahrs.yaw - starting_yaw1 - yaw1_shift*loop)/1.13)*3.14/180 - yaw1_blah)
	pitch1_rad = yInvert * (((wiimote[0].ahrs.pitch - starting_pitch1 - pitch1_shift*loop)/1.13)*3.14/180 - pitch1_blah)
	roll1_rad = yInvert * (((wiimote[0].ahrs.roll - starting_roll1 - roll1_shift*loop)/1.13)*3.14/180 - roll1_blah)
	
	diagnostics.watch((yaw1_rad, pitch1_rad, roll1_rad))
	
	alvr.controller_orientation[0][0] = math.fmod(yaw1_rad, math.pi*2)
	alvr.controller_orientation[0][1] = math.fmod(-pitch1_rad*math.cos(yaw1_rad), math.pi*2)
	alvr.controller_orientation[0][2] = math.fmod(-pitch1_rad * math.sin(yaw1_rad), math.pi*2)
	
	alvr.controller_position[0][0] = scale1*(math.sin(yaw1_rad - 0.5*math.pi)*300 - 150)
	alvr.controller_position[0][1] = scale1*(-math.cos(yaw1_rad - 0.5*math.pi)*300 - 150)
	alvr.controller_position[0][2] = 740 + -math.sin(pitch1_rad)*900
	
	if wiimote[0].buttons.button_down(WiimoteButtons.Plus):
		scale1 = 1
	alvr.buttons[0][alvr.Id("start")] = wiimote[0].buttons.button_down(WiimoteButtons.Minus)
	
	if wiimote[0].buttons.button_down(WiimoteButtons.B):
		alvr.buttons[0][alvr.Id("trigger")] = 1.0
	else:
		alvr.buttons[0][alvr.Id("trigger")] = 0
	
	if wiimote[0].buttons.button_down(WiimoteButtons.DPadUp):
		scale1 += 0.003
	if wiimote[0].buttons.button_down(WiimoteButtons.DPadDown):
		scale1 -= 0.003
	#####
	
	
	yaw2_rad = xInvert * (((wiimote[1].ahrs.yaw - starting_yaw2 - yaw2_shift*loop)/1.13)*3.14/180 - yaw2_blah)
	pitch2_rad = yInvert * (((wiimote[1].ahrs.pitch - starting_pitch2 - pitch2_shift*loop)/1.13)*3.14/180 - pitch2_blah)
	roll2_rad = yInvert * (((wiimote[1].ahrs.roll - starting_roll2- roll2_shift*loop)/1.13)*3.14/180 - roll2_blah)
	
	diagnostics.watch((yaw2_rad, pitch2_rad, roll2_rad))
	
	alvr.controller_orientation[1][0] = math.fmod(yaw2_rad, math.pi*2)
	alvr.controller_orientation[1][1] = math.fmod(-pitch2_rad*math.cos(yaw2_rad), math.pi*2)
	alvr.controller_orientation[1][2] = math.fmod(-pitch2_rad * math.sin(yaw2_rad), math.pi*2)
	
	alvr.controller_position[1][0] = scale2*(math.sin(yaw2_rad - 0.5*math.pi)*300 - 150)
	alvr.controller_position[1][1] = scale2*(-math.cos(yaw2_rad - 0.5*math.pi)*300 - 150)
	alvr.controller_position[1][1] = 740 + -math.sin(pitch2_rad)*900
	
	if wiimote[0].buttons.button_down(WiimoteButtons.Plus):
		scale2 = 1
	alvr.buttons[1][alvr.Id("start")] = wiimote[1].buttons.button_down(WiimoteButtons.Minus)
	
	if wiimote[1].buttons.button_down(WiimoteButtons.B):
		alvr.buttons[1][alvr.Id("trigger")] = 1.0
	else:
		alvr.buttons[1][alvr.Id("trigger")] = 0
	
	
	if wiimote[1].buttons.button_down(WiimoteButtons.DPadUp):
		scale2 += 0.003
	if wiimote[1].buttons.button_down(WiimoteButtons.DPadDown):
		scale2 -= 0.003
		
	if wiimote[0].buttons.button_down(WiimoteButtons.Home):
		starting_yaw1, starting_pitch1, starting_roll1 = wiimote[0].ahrs.yaw - yaw1_shift*loop, wiimote[0].ahrs.pitch - pitch1_shift*loop, wiimote[0].ahrs.roll - roll1_shift*loop
	if wiimote[1].buttons.button_down(WiimoteButtons.Home):
		starting_yaw2, starting_pitch2, starting_roll2 = wiimote[1].ahrs.yaw - yaw2_shift*loop, wiimote[1].ahrs.pitch - pitch2_shift*loop, wiimote[1].ahrs.roll - roll2_shift*loop
	
	
	
	
diagnostics.watch("borke")
diagnostics.watch((wiimote[1].ahrs.yaw, wiimote[1].ahrs.pitch, wiimote[1].ahrs.roll))
diagnostics.watch((wiimote[0].ahrs.yaw, wiimote[0].ahrs.pitch, wiimote[0].ahrs.roll))

if keyboard.getKeyDown(Key.Space):
	
	old_yaw1 = wiimote[0].ahrs.yaw
	old_pitch1 = wiimote[0].ahrs.pitch
	old_roll1 = wiimote[0].ahrs.roll
	
	old_yaw2 = wiimote[1].ahrs.yaw
	old_pitch2 = wiimote[1].ahrs.pitch
	old_roll2 = wiimote[1].ahrs.roll
	
	starting_yaw1, starting_pitch1, starting_roll1 = old_yaw1, old_pitch1, old_roll1
	starting_yaw2, starting_pitch2, starting_roll2 = old_yaw2, old_pitch2, old_roll2	
	
	yaw1 = yaw2 = 0
	pitch1 = pitch2 = 0
	roll1 = roll2 = 0
	
	yaw1_shift = []
	pitch1_shift = []
	roll1_shift = []
	
	yaw2_shift = []
	pitch2_shift = []
	roll2_shift = []

	loop = 0
	
	alvr.controller_orientation[0][0] = 0
	alvr.controller_orientation[0][1] = 0
	alvr.controller_orientation[0][2] = 0
	
	alvr.controller_position[0][0] = 0
	alvr.controller_position[0][1] = 0
	alvr.controller_position[0][2] = 0
	
	alvr.controller_orientation[1][0] = 0
	alvr.controller_orientation[1][1] = 0
	alvr.controller_orientation[1][2] = 0
	
	alvr.controller_position[1][0] = 0
	alvr.controller_position[1][1] = 0
	alvr.controller_position[1][2] = 0
	
	yaw1_blah = pitch1_blah = roll1_blah = yaw2_blah = pitch2_blah = roll2_blah = 0
	scale1 = scale2 = 1

alvr.buttons[0][alvr.Id("grip")]  = wiimote[0].buttons.button_down(WiimoteButtons.A)
alvr.buttons[1][alvr.Id("grip")]  = wiimote[1].buttons.button_down(WiimoteButtons.A)