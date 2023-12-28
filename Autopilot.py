import time
import krpc

conn = krpc.connect()

vessel = conn.space_center.active_vessel

#Flight State
accentPhase = True
cruisePhase = False
insertionPhase = False

while accentPhase or cruisePhase or insertionPhase:
    altitude = vessel.flight().mean_altitude
    heading = vessel.flight().heading
    
    if accentPhase:
        targetPitch = 90 * ((50000 - altitude) / 50000)
        pitchDiff = vessel.flight().pitch - targetPitch

        #Heading Control
        if heading < 180:
            vessel.control.yaw = (pitchDiff / 90)
        else:
            vessel.control.yaw = 0.5

        #Staging
        if vessel.thrust == 0.0:
            vessel.control.activate_next_stage()

        #MECO
        if vessel.orbit.apoapsis > 690000:
            vessel.control.throttle = 0
            time.sleep(0.5)
            vessel.control.activate_next_stage()

            vessel.control.sas = True
            time.sleep(0.1)
            vessel.control.sas_mode = conn.space_center.SASMode.prograde

            accentPhase = False
            cruisePhase = True
    elif cruisePhase:
        if altitude > 80000:
            cruisePhase = False
            insertionPhase = True
            vessel.control.sas = False
            vessel.control.throttle = 1
    elif insertionPhase:
        targetPitch = 0
        pitchDiff = vessel.flight().pitch - targetPitch

        #Heading Control
        if heading < 180:
            vessel.control.yaw = (pitchDiff / 90)
            if vessel.flight().pitch < 1 and vessel.flight().pitch > -1:
                vessel.control.sas = True
            else:
                vessel.control.sas = False
        else:
            vessel.control.yaw = 0.5

        #SECO
        if vessel.orbit.periapsis > 690000:
            vessel.control.throttle = 0
            insertionPhase = False

        #Staging
        if vessel.thrust == 0.0:
            vessel.control.activate_next_stage()

