from random import randint
import json


class Query:
    query_type = 0
    time = 0
    name = ""

    def __init__(self, name):
        """
        Создание экземляра запроса к процессору
        :param name: имя запроса
        :type name: str
        """
        self.query_type = randint(0, 2)
        self.name = name + "@" + str(self.query_type)
        self.time = randint(2, 10)

    def get_info(self):
        data = {
            'name': self.name,
            'query_type': self.query_type,
            'time': self.time,
        }
        return json.dumps(data)