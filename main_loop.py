import json
import time
from rpi_ws281x import *
from src.interfaces.Connection import Connection
from src.instructions.instruction import Instruction
from src.interfaces import Treads
from src.interfaces import Arm
from src.interfaces import Camera
from src.interfaces import LED
from src.interfaces import DistanceSensor

# JOSE'S HOTSPOT
# Jose_laptop = "192.168.43.116"
# SeanR_laptop = "192.168.43.156"
# SeanD_laptop = "192.168.43.68"
# SeanD_laptop_linux = "192.168.0.26"
# LOCAL_HOST = "127.0.0.1"

# TUSECUREWIRELESS
# BinBot = 10.108.92.75
SeanR_laptop = "10.108.22.58"

IP = SeanR_laptop
PORT = 7001
LED = LED.LED()
camera = Camera.Camera()


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


try:
    while True:
    # try:
        LED.colorWipe(Color(0, 0, 255))  # LED BLUE

        # Capture picture
        cur_t0 = time.time()
        print("Capturing image..")
        Arm.home()  # Move arm out of camera view
        img = camera.capture_image()
        distance = DistanceSensor.checkdistance()
        print(f"Distance: {distance}")
        instr_out = Instruction(Instruction.FROM_DATA, "PATROL", img, distance, None)

        # Send image to server
        connection = Connection(IP, PORT)
        print("Sending image to server")
        connection.send(instr_out.instructionToJson())

        msg_in = connection.receive()
        print("Received image from server")
        connection.close()

        print(f"exhcange time: {time.time() - cur_t0}")

        print(msg_in)
        if is_json(msg_in):
            instr_in = Instruction(Instruction.FROM_JSON, msg_in)
            status = instr_in.status()
            treads = instr_in.treads()
            if treads is not None:
                # print(treads)
                try:
                    Treads.setup()
                    for movement in treads:
                        LED.colorWipe(Color(255, 16, 0))  # LED RED
                        print(f"Exe: {movement}")
                        # RETREIVE OBJECT
                        if movement["angle"] == 0.0 and movement["distance"] == 1.0:
                            LED.colorWipe(Color(0, 225, 0))  # LED GREEN
                            Treads.moveBySensor()
                            # x = DistanceSensor.checkdistance()
                            # print(f"dist1: {x}")
                            # x = (x*10) - 1.0
                            # print(f"dist2: {x}")
                            # new_movement = {"angle": 0, "distance": x}
                            # Treads.executeTreadInstruction(new_movement)

                            print("PICK UP")
                            Arm.pick_up()
                        else:
                            print("skipping")
                            # Treads.executeTreadInstruction(movement)
                    Treads.destroy()
                    Arm.clean_all()
                except Exception as e:
                    print("Instruction execution exception: %s", e)
                    Treads.destroy()
                    Arm.clean_all()
                    LED.colorWipe(Color(0, 0, 0))

            else:
                print('No treads')

except Exception as e:
    print("Exeption throw: %s", e)
    Treads.destroy()
    Arm.clean_all()
    LED.colorWipe(Color(0, 0, 0))
