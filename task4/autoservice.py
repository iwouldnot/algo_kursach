class Autoservice:
    def __init__(self, id, name, owner, city):
        self.id = id
        self.name = name
        self.owner = owner
        self.city = city

    def __repr__(self):
        return 'ID: {id}; \'{name}\' autoservice in {city}, by {owner}'.format(id=self.id, name=self.name, city=self.city, owner=self.owner)

    def __eq__(self, other):
        try:
            return self.id == other.id
        except:
            return False

    def __ne__(self, other):
        return self.id != other.id

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id