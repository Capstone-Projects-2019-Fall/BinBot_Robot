# Author: Sean DiGirolamo
# Date: 10/3/2019

import json


class Instruction:
    def __init__(self, status, img=None, treads=None, arms=None):
        if img is None and treads is None and arms is None:
            obj = json.loads(status)
            self.__status = obj["status"]
            self.__img = obj["img"]
            self.__treads = obj["treads"]
            self.__arms = obj["arms"]
        else:
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

    def status(self):
        return self.__status

    def img(self):
        return self.__img

    def treads(self):
        return self.__treads

    def arms(self):
        return self.__arms
