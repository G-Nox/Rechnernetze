import heapq


class Eventqueue:
    eventNr = 0

    def __init__(self):
        self.eventHQ = []

    def pop(self):
        return heapq.heappop(self.eventHQ)

    def push(self, event):
        heapq.heappush(self.eventHQ, event)

    def start(self):
        while len(self.eventHQ) > 0:
            event = self.pop()
            last_customer = event[3](self, event)
        last_customer.result.simu_end_time = event[0]
        return last_customer.result
