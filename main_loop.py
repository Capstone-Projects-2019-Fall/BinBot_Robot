import json

from src.interfaces.Connection import Connection
from src.instructions.instruction import Instruction
from src.interfaces import Treads
# from src.interfaces import Camera


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


IP = "192.168.43.68"
PORT = 7001

camera = None
arm = None

while True:

    # img = camera.take_photo()

    instr_out = Instruction(Instruction.FROM_DATA, "PATROL", None, None, None)

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
                    Treads.executeTreadInstruction(movement)
                    print()
                Treads.destroy()
            except Exception as e:
                print("Tread exception: %s", e)
                Treads.destroy()

        else:
            print('No treads')
