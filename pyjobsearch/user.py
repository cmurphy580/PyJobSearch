import random


class User():
    def __init__(self):
        self.username = None
        self.password = None
        self.ID = random.randint(10000, 999999)
        self.favorites = []

    def __eq__(self, other): 
        return self.username is other["username"] and self.password is other["password"]

    def to_dict(self):
        return {"username": self.username, "password": self.password,
                "ID": self.ID, "favorites": self.favorites}
