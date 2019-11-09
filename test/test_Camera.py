import json
import unittest
from src.interfaces import Camera

class TestInstruction(unittest.TestCase):

    def setUp(self):
        pass

    def test_execute(self):
        try:

            Camera.take_photo()

        except Exception as e:
            print("Camera exception: %s", e)


if __name__ == '__main__':
    unittest.main()