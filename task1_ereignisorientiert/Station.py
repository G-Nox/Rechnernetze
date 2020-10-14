from collections import deque


class Station:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.queue = deque([])
        self.isOperate = False

    def arrival(self, customer):
        self.queue.append(customer)
        self.isOperate = True

    def leave(self, customer):
        self.queue.remove(customer)
        if len(self.queue) == 0:
            self.isOperate = False
