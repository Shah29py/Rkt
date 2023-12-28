## Запись всех данных из KSP
import csv
import krpc
import time

fields = ['Time', 'Velocity', 'GForce', 'Accelaration', 'Thrust', 'TWR', 'AltitudeFromTerrain', 'AltitudeFromSea',
          'DownrangeDistance', 'Latitude', 'Longitude', 'Apoapsis', 'Periapsis', 'Inclination', 'OrbitalVelocity',
          'TargetDistance', 'TargetVelocity', 'StageDeltaV', 'VesselDeltaV']
rows = []

with open('stats.csv', 'a') as f:
    write = csv.writer(f)

    write.writerow(fields)

    conn = krpc.connect()
    vessel = conn.space_center.active_vessel
    srf_frame = vessel.orbit.body.reference_frame
    cur_time = 0
    prev_srf_speed = 0
    # node = conn.space_center.active_vessel.control.add_node('ut')

    while True:
        srf_speed = vessel.flight(srf_frame).speed
        altitude = vessel.flight(srf_frame).surface_altitude
        gforce = vessel.flight(srf_frame).g_force
        acelaration = srf_speed - prev_srf_speed
        thrust = sum(engine.thrust for engine in vessel.parts.engines)
        twr = thrust / (9.81 * vessel.mass)
        altitudeFromSea = vessel.flight(srf_frame).mean_altitude
        latitude = vessel.flight(srf_frame).latitude
        longitude = vessel.flight(srf_frame).longitude
        apoapsis = conn.space_center.active_vessel.orbit.apoapsis
        periapsis = conn.space_center.active_vessel.orbit.periapsis
        inclination = conn.space_center.active_vessel.orbit.inclination
        orbital_velocity = conn.space_center.active_vessel.orbit.speed

        rows.append(
            [cur_time, srf_speed, gforce, acelaration, thrust, twr, altitude, altitudeFromSea, 0, latitude, longitude,
             apoapsis, periapsis, inclination, orbital_velocity])

        write.writerows(rows)

        prev_srf_speed = srf_speed

        cur_time += 1
        rows = []
        time.sleep(1)


