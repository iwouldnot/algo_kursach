import pandas as pd
from processor import Processor
from customqueue import CustomQueue
from stack import Stack
from query import Query
import json


def decode(json_string):
    return json.loads(json_string)


def main():
    total_number_of_queries = 10000
    queries = CustomQueue()
    # for i in range(number_of_queries):
    #     queries.enqueue(Query("query{}".format(i)))
    processors = [Processor("P0"), Processor("P1"), Processor("P2")]
    awaiting_queries = Stack()

    def system_awaits():
        return processors[0].is_free \
               and processors[1].is_free \
               and processors[2].is_free \
               and awaiting_queries.is_empty() \
               and queries.is_empty()

    def fancy_status(processor):
        try:
            json_status = processor.get_status()
            parsed_status = decode(json_status)
            if not parsed_status['is_free']:
                return "{}: Query \"{:5}\"; Time remaining: {:2}".format(parsed_status['processor_name'],
                                                                         parsed_status['current_query'],
                                                                         parsed_status['time_left_for_query'])
        except AttributeError:
            return "{}: currently free.".format(processor.name)

    def get_processor_state(processor):
        try:
            return fancy_status(processor)
        except AttributeError:
            return "free"

    query_number = 0
    queries.enqueue(Query(str(query_number)))
    query_number += 1
    f = open('report.txt', 'w', encoding='utf-8')

    size_of_stack = []
    p0_is_free = []
    p1_is_free = []
    p2_is_free = []

    while not system_awaits():
        if not queries.is_empty():
            new_query = queries.dequeue()
            # print(new_query.get_info(), ' ', query_number)
            f.write('Generated: ')
            f.write(new_query.get_info())
            f.write('\n')
            if processors[new_query.query_type].is_free:
                processors[new_query.query_type].set_task(new_query)
            else:
                awaiting_queries.push(new_query)

        if not awaiting_queries.is_empty():
            f.write('Top of stack: ')
            f.write(awaiting_queries.peek().get_info())
            f.write('\n')
            if processors[awaiting_queries.peek().query_type].is_free:
                processors[awaiting_queries.peek().query_type].set_task(awaiting_queries.pop())

        for i in processors:
            # print(fancy_status(i))
            f.write(fancy_status(i) + '\n')
            i.next_tick()
        # print('-' * 80)
        f.write('-' * 80 + '\n')

        if query_number < total_number_of_queries:
            queries.enqueue(Query(str(query_number)))
            query_number += 1

        size_of_stack.append(awaiting_queries.size())
        p0_is_free.append(processors[0].is_free)
        p1_is_free.append(processors[1].is_free)
        p2_is_free.append(processors[2].is_free)

    df = pd.DataFrame({
        'stack_size': size_of_stack,
        'p0_is_free': p0_is_free,
        'p1_is_free': p1_is_free,
        'p2_is_free': p2_is_free
    })
    df.to_csv('raw_data.csv')



if __name__ == '__main__':
    main()