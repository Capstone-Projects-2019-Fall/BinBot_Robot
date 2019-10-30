from unittest import TestCase

from src.instruction import Instruction

JSON_STRING = '{"status":"PATROL","img":"temporary","treads":[{"angle":0.0,"distance":1.1}],"arms":[{"angle":2.2}]}'
STATUS = 'PATROL'
IMG = 'temporary'
TREADS = [{"angle": 0.0, "distance": 1.1}]
ARMS = [{"angle": 2.2}]

class TestInstruction(TestCase):
    def __init__(self):
        super().__init__()
        self.json_obj = Instruction(JSON_STRING)
        self.data_obj = Instruction()

    def test_json(self):
        self.fail()

    def test_status(self):
        self.fail()

    def test_img(self):
        self.fail()

    def test_treads(self):
        self.fail()

    def test_arms(self):
        self.fail()
