import json
import time
from src.interfaces.Connection import Connection
from src.instructions.instruction import Instruction
from src.interfaces import Treads
from src.interfaces import Camera
from src.interfaces.DistanceSensor import checkdistance

Jose_laptop = "192.168.43.116"
SeanR_laptop = "192.168.43.156"
SeanD_laptop = "192.168.43.68"
SeanD_laptop_linux = "192.168.0.26"
LOCAL_HOST = "127.0.0.1"

IP = SeanR_laptop
PORT = 7001

camera = Camera.Camera()
arm = None


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


while True:

    cur_t0 = time.time()
    print("Capturing image..")
    img = camera.capture_image()
    distance = checkdistance()
    print(f"Distance: {distance}")
    instr_out = Instruction(Instruction.FROM_DATA, "PATROL", img, distance, None)

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
                    print(f"Exe: {movement}")
                    if movement["angle"] == 0.0 and movement["distance"] == 1.0:
                        x = checkdistance()
                        print(f"dist: {x}")
                        new_movement = {"angle": 0, "distance": 2.0}
                        Treads.executeTreadInstruction(new_movement)
                        print("PICK UP")
                    else:
                        print("skipping")
                        # Treads.executeTreadInstruction(movement)
                    print()
                Treads.destroy()
            except Exception as e:
                print("Tread exception: %s", e)
                Treads.destroy()

        else:
            print('No treads')
