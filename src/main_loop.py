from src.interfaces.Connection import Connection
from src.instructions.instruction import Instruction
from src.interfaces.Treads import Treads
from src.interfaces.Camera import Camera

IP = "127.0.0.1"
PORT = 7001

connection = Connection(IP, PORT)
camera = None
treads = Treads()
arm = None

while True:

    # img = camera.take_photo()

    instr_out = Instruction(Instruction.FROM_DATA, "PATROL", None, None, None)
    connection.send(instr_out.json())

    msg_in = connection.receive()
    instr_in = Instruction(Instruction.FROM_JSON, msg_in)
    status = instr_in.status()
    if instr_in.treads() is not None:
        print(instr_in.treads())
        treads.execute(instr_in.treads())
    else:
        print('No treads')
