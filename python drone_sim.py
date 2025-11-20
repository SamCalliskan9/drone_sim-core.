
... import random
... import time
... 
... def clamp(v, lo, hi):
...     return max(lo, min(hi,v))
... 
... def status(drone):
...     print("\n--- STATUS ---")
...     print(f"Pos (x,alt): {drone['x']:.1f}, {drone['z']:.1F}) | Battery: {drone['battery']:.0f}% | Stability: {drone['stability']:.0f}")
...     print(f" Wind: {drone['wind']:.1f} m/s | Speed: {drone['vx']:.1f} m/tick")
...     print(f"Mission: {drone['mission']}")
...     print("----------------\n")
... 
... def update_wind(drone):
... 
...     gust = random.uniform(-1.0, 1.0)
...     if random.random() < 0.1:
...         gust += random.choice([-1.5, 1.5])
...     drone['wind'] = clamp(drone['wind'] * 0.7 + gust * 0.3, -5.0, 5.0)
... 
... def apply_command(cmd, drone):
...     """
...     cmd: 'ascend, 'descend', 'forward', 'hover', 'land'
...     Simplified physics: ascend/descend change altitude; forward changes x; hover stabilizes.
...     Battery cost and stability effects applied.
...     """
...     if cmd == 'ascend':
...         drone['vz'] += 1.0
...         drone['battery'] -= 4.0
...         drone['stability'] -= abs(drone['wind']) * 1.2
...     elif cmd == 'descend':
...         drone['vz'] -= 1.0
...         drone['battery'] -= 2.0
...         drone['stability'] -= abs(drone['wind']) * 0.8
    elif cmd == 'forward':
        drone['vx'] += 1.0
        drone['battery'] -= 3.5
        drone['stability'] -= abs(drone['wind']) * 1.0
    elif cmd == 'hover':

        drone['battery'] -= 2.5
        drone['stability'] += 3.0 - abs(drone['wind'])
    elif  cmd == 'land':

        drone['vz'] = -2.5
        drone['battery'] -= 1.5
        drone['stability'] -= abs(drone['wind']) * 1.5
    else:
        print("Unknown command. Doing nothing.")
        drone['battery'] -= 0.5

def physics_tick(drone):

    drone['vx'] += drone['wind'] * 0.05

    drone["x"] += drone['vx']
    drone['z'] += drone['vz']

    if drone['z'] < 0:
        drone['z'] = 0
    if drone['z'] > 100:
        drone['z'] = 100

    drone['vx'] *= 0.9
    drone['vz'] *= 0.6

    drone['battery'] -= 0.2

    drone['battery'] = clamp(drone['battery'], 0.0, 100.0)
    drone['stability'] = clamp(drone['stability'], 0.0, 100.0)

def check_failures(drone):

    if drone['stability'] < 15:
        if drone['battery'] < 0.25:
            print("\n!!! Critical İnstability' Drone spins out of control and crashes !!!")
            return 'crash'

    if drone['battery'] <= 0 and drone['z'] > 2:
        print("\n!!! battery depleted mid-air! Drone falls and crashes!!!")
        return 'crash'

    if drone['z'] == 0 and abs(drone['vz']) > 3.0:
        print("\n!!! Hard landing! Drone damaged and mission failed. !!!")
        return 'crash'
    return None

def mission_check(drone):

    target_x = drone['target_x']
    if drone['x'] >= target_x and drone['z'] == 0:
        return 'success'
    return None

def help_text():
    print("Commands: ascend | descend | forward | hover | land | status | help | quit")
    print("Goal: reach target x coordinate and land safely. Manage battery and stability.")
    print("Tip: 'hover' stabilizes in low wind. 'ascend' to avoid obstacle; 'land' to touch down.")

def main():
    print("=== Drone Flight Simulator (turn-based) ===")
    pilot = input("Pilot name: ").strip() or "Pilot"
    print(f"Welcome, {pilot}. Starting mission briefing...\n")
    time.sleep(0.6)

    drone = {
        'x': 0.0,
        'z': 0.0,
        'vx': 0.0,
        'vz': 0.0,
        'battery': 100.0,
        'stablity': 80.0,
        'wind': 0.0,
        'mission': 'deliver package to X',
        'target_x': random.uniform(30.0, 60.0)
    }

    print(f"Mission: reach X = {drone['target_x']:.1f} and perform a safe landing.")
    print("İnitialize launch sequence: ascend to safe altitude (z>2), then move forward.")
    help_text()

    tick = 0
    while True:
        tick += 1
        update_wind(drone)
        cmd = input("\nEnter command: ").strip().lower()

        if cmd == 'quit':
            print("Mission aborted by pilot.")
            break
        if cmd == 'help':
            help_text()
            continue
        if cmd == 'status':
            status(drone)
            continue

        apply_command(cmd, drone)
        physics_tick(drone)

        if abs(drone['wind']) < 0.3 and cmd == 'hover':
            drone['stability'] = clamp(drone['stability'] + 1.5, 0,100)

        if random.random() < 0.05:
            print(" Unexpected event: small bird strike! Stability reduced.")
            drone['stability'] -= random.uniform(5,12)

        fall = check_failures(drone)
        if fall == 'crash':
            print("Mission failed.")
            break

        result = mission_check(drone)
        if result == 'success' :
            print("\n*** TARGET REACHED AND LANDED SAFELY! MISSION SUCCESSFUL! ***")
            print(f"pilot {pilot}, well done. Final stats:")
            status(drone)
            break

        if tick % 3 == 0:
            status(drone)

        time.sleep(0.15)

if __name__ == '__main__':
    main()



