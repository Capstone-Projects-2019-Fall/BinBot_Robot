# Author: Sean DiGirolamo
# Date: 10/3/2019

import json


class Instruction:
    def __init__(self, string):
        obj = json.loads(string)
        self.__status = obj["status"]
        self.__img = obj["img"]
        self.__treads = obj["treads"]
        self.__arms = obj["arms"]

    def _init_(self, status, img, treads, arms):
        self.__status = status
        self.__img = img
        self.__treads = treads
        self.__arms = arms

    def json(self):
        retval = '{"status":"' + self.__status + '",'
        retval += '"img":"' + self.__img + '",'
        retval += '"treads":['
        for x in self.__treads:
            retval += '{"angle":' + x["angle"] + ','
            retval += '"distance":' + x["distance"] + '}'
            if x != self.__treads[-1]:
                retval += ','
        retval += '],'
        retval += '"arms":['
        for x in self.__arms:
            retval += '{"angle":' + x["angle"] + '}'
            if x != self.__treads[-1]:
                retval += ','
        retval += ']}'
        return retval

    def __img_to_string(self):
        pass

    def