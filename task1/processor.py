from query import Query
import json


class Processor:
    is_free = True
    current_query = None
    time_left_for_query = 0
    name = ""

    def __init__(self, name):
        self.name = name

    def set_task(self, task: Query):
        self.is_free = False
        self.current_query = task
        self.time_left_for_query = task.time

    def next_tick(self):
        if self.time_left_for_query == 1:
            self.is_free = True
            self.current_query = None
            name = ""
        self.time_left_for_query -= 1

    def get_status(self):
        data = {
            'is_free': self.is_free,
            'current_query': self.current_query.name,
            'time_left_for_query': self.time_left_for_query,
            'processor_name': self.name
        }
        return json.dumps(data)