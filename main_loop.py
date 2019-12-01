import json

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

    img = camera.capture_image()
    instr_out = Instruction(Instruction.FROM_DATA, "PATROL", img, None, None)

    connection = Connection(IP, PORT)
    connection.send(instr_out.json())
    msg_in = connection.receive()
    connection.close()

    print(msg_in)
    if is_json(msg_in):
        instr_in = Instruction(Instruction.FROM_JSON, msg_in)
        status = instr_in.status()
        if instr_in.treads() is not None:
            print(instr_in.treads())
            try:
                Treads.setup()
                for movement in instr_in.treads():
                    if movement["angle"] == 0:
                        x = checkdistance()
                        new_movement = {"angle": 0, "distance": x}
                        Treads.executeTreadInstruction(new_movement)
                    else:
                        Treads.executeTreadInstruction(movement)
                    print()
                Treads.destroy()
            except Exception as e:
                print("Tread exception: %s", e)
                Treads.destroy()

        else:
            print('No treads')
