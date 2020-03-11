#!/usr/bin/env python3

import sys
import socket
import time
try:
    import ev3dev.ev3 as ev3
    use_ev3 = True
except:
    use_ev3 = False
    pass

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1:3]
HOST = host
PORT = int(port)
#HOST = "127.0.0.1"  # The server's hostname or IP address
#PORT = 65432  # The port used by the server

if use_ev3:
    i = ev3.LargeMotor('outA')
    m = ev3.LargeMotor('outB')
    r = ev3.LargeMotor('outC')
    p = ev3.LargeMotor('outD')
    if not (m.connected):
        print("Plug the pointer motor into Port A")
        sys.exit(1)
    else:
        print("Motor connected.")
    #m.run_to_rel_pos(position_sp=100,speed_sp=50)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while True:
        try:
            s.connect((HOST, PORT))
            print("Connected to server!")
            break
        except Exception as e:
            print(repr(e))
            print(HOST + ":" + str(PORT) + " Address inaccessible, trying again in 5s")
            time.sleep(5)
    while True:
        data = s.recv(1024)
        if not data:
            break
        else:
            print("Received " + repr(data))
        if data == b'i_forward':
            print("Moving index forward")
            if use_ev3:
                i.run_to_rel_pos(position_sp=50,speed_sp=50)
        elif data == b'i_backward':
            print("Moving index backward")
            if use_ev3:
                i.run_to_rel_pos(position_sp=-80,speed_sp=50)
        if data == b'm_forward':
            print("Moving middle forward")
            if use_ev3:
                m.run_to_rel_pos(position_sp=80,speed_sp=50)
        elif data == b'm_backward':
            print("Moving middle backward")
            if use_ev3:
                m.run_to_rel_pos(position_sp=-80,speed_sp=50)
        elif data == b'r_forward':
            print("Moving ring forward")
            if use_ev3:
                r.run_to_rel_pos(position_sp=80,speed_sp=50)
        elif data == b'r_backward':
            print("Moving ring backward")
            if use_ev3:
                r.run_to_rel_pos(position_sp=-80,speed_sp=50)
        elif data == b'p_forward':
            print("Moving pinky forward")
            if use_ev3:
                p.run_to_rel_pos(position_sp=80,speed_sp=50)
        elif data == b'p_backward':
            print("Moving pinky backward")
            if use_ev3:
                p.run_to_rel_pos(position_sp=-80,speed_sp=50)

