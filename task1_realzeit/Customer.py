import threading
import time


class Customer(threading.Thread):

    def __init__(self, stationsWithType, name, result, start_time):
        threading.Thread.__init__(self)
        self.stationsWithType = stationsWithType
        self.name = name
        self.result = result
        self.start_time = start_time

    def run(self):
        # start_time = actual_time
        self.result.count_customers += 1
        while len(self.stationsWithType) != 0:
            stationWithType = self.stationsWithType.pop()
            station = stationWithType[0]
            type = stationWithType[1]
            # Zeit bis zur Station
            time.sleep(type[0])

            if len(station.queue) < type[2]:
                print(f"{time.time() - self.start_time:.2f}: " + self.name + " Queueing at " + station.name)
                servEv = threading.Event()
                station.arrival((type[1], servEv, self))
                station.arrEv.set()
                servEv.wait()
            else:
                print(f"{time.time() - self.start_time:.2f}: " + self.name + " Dropped at " + station.name)
                self.result.dropped_customers += 1
                self.result.drop_station_dict[station] += 1

        # self.result.mediator_period_list.append(actual_time - start_time)
