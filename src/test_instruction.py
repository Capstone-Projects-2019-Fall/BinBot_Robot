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
        self.data_obj = Instruction(STATUS, IMG, TREADS, ARMS)

    def test_json(self):
        assert self.json_obj.json() == JSON_STRING
        assert self.data_obj.json() == JSON_STRING
        self.fail()

    def test_status(self):
        assert self.json_obj.status() == STATUS
        assert self.data_obj.status() == STATUS
        self.fail()

    def test_img(self):
        assert self.json_obj.img() == IMG
        assert self.data_obj.img() == IMG
        self.fail()

    def test_treads(self):
        assert self.json_obj.treads() == TREADS
        assert self.data_obj.treads() == TREADS
        self.fail()

    def test_arms(self):
        assert self.json_obj.arms() == ARMS
        assert self.data_obj.arms() == ARMS
        self.fail()
