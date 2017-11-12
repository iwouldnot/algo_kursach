from autoservice import Autoservice
import random
import string
import itertools

id_operator = itertools.count()


def create_random_autoservice():
    def random_word(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    id = id_operator.__next__()
    name = random_word(random.randint(3, 10))
    owner = random_word(random.randint(5, 10))
    city = random_word(random.randint(3, 8))
    a = Autoservice(id, name, owner, city)
    return a
