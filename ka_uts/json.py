# coding=utf-8

# import orjson
import ujson
import json

from typing import NewType
from typing import Dict, List, Union

AoD = NewType('AoD', List[Dict])
Value = NewType('Value', Union[str, List, Dict])


class Json:

    @staticmethod
    def loads(obj, **kwargs):
        json_type = kwargs.get('json_type', 'orjson')
        if json_type == 'ujson':
            obj = ujson.loads(obj)
        else:
            obj = json.loads(obj)
        return obj

    @staticmethod
    def dumps(obj, **kwargs):
        json_type = kwargs.get('json_type', 'orjson')
        indent = kwargs.get('indent')
        if json_type == 'ujson':
            ujson.dumps(obj, indent=indent)
        else:
            json.dumps(obj, indent=indent)
        return obj

    @classmethod
    def write(cls, obj, path_, **kwargs):
        json_type = kwargs.get('json', 'orjson')
        indent = kwargs.get('indent', 2)
        if json_type == 'orjson':
            # json_byte = orjson.dumps(
            #   obj, option=orjson.OPT_INDENT_2, **kwargs)
            # with open(path_, 'wb') as fd:
            #     fd.write(json_byte)
            with open(path_, 'w') as fd:
                json.dump(obj, fd, indent=indent, **kwargs)
        if json_type == 'ujson':
            with open(path_, 'w') as fd:
                json.dump(obj, fd, indent=indent, **kwargs)
        else:
            with open(path_, 'w') as fd:
                json.dump(obj, fd, indent=indent, **kwargs)

    @staticmethod
    def read(path_file, **kwargs):
        mode = kwargs.get('mode', 'rb')
        json_type = kwargs.get('json', 'orjson')
        with open(path_file, mode) as fd:
            if json_type == 'orjson':
                # obj = orjson.loads(fd.read())
                obj = ujson.loads(fd.read())
            elif json_type == 'ujson':
                obj = ujson.loads(fd.read())
            else:
                obj = json.loads(fd.read())
            return obj
        return None
