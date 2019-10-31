from src.interfaces.Connection import Connection
from src.json.instruction import Instruction

IP = "127.0.0.1"
PORT = 7001

connection = Connection(IP, PORT)
camera = None
treads = None
arm = None

while True:
    msg_in = connection.receive()
    instr_in = Instruction(msg_in)
    status = instr_in.status()
    if status == "PATROL":
        # arm.patrol()
        pass
    else:  # status == "NAVIGATE"
        # treads.exec(instr_in.treads)
        # arms.exec(instr_in.arms)
        pass
    # img = camera.capture_img()
    # instr_out = Instruction("PATROL", img, None, None)
    # connection.send(instr_out.json())
