class Customer:
    start_time = 0

    def __init__(self, stationsWithType, name, result):
        self.stationsWithType = stationsWithType
        self.name = name
        self.result = result

    # Ereignis Ankunft an erster Station erzeugen
    def start(self, eventqueue, event):
        self.result.count_customers += 1
        self.start_time = event[0]
        if len(self.stationsWithType) == 4:     # typ 1
            eventqueue.push((event[0]+self.stationsWithType[len(self.stationsWithType) - 1][1][0], 1, eventqueue.eventNr, self.arrival))
        else:                                   # typ 2
            eventqueue.push((event[0]+self.stationsWithType[len(self.stationsWithType) - 1][1][0], 1, eventqueue.eventNr, self.arrival))

        eventqueue.eventNr += 1

    def arrival(self, eventqueue, event):
        stationWithType = self.stationsWithType[len(self.stationsWithType) - 1]
        station = stationWithType[0]
        type = stationWithType[1]
        eventtime = event[0] + station.duration * type[1]

        # Überprüfen ob eingekauft wird
        if len(station.queue) == 0:             # Schlange leer -> Ereignis verlassen der Station erzeugen
            station.arrival(self)
            eventqueue.push((eventtime, 0, eventqueue.eventNr, self.leave))
            eventqueue.eventNr += 1
            # Ausgabe
            print(str(event[0]) + ":" + self.name + " Queueing at " + station.name)
        else:
            if len(station.queue) > type[2]:    # Schlange zu groß -> auslassen
                eventtime = event[0]+self.stationsWithType[len(self.stationsWithType) - 1][1][0]    # aktuelle zeit + zeit bis zur nächsten station
                self.stationsWithType.pop()
                eventqueue.push((eventtime, 1, eventqueue.eventNr, self.arrival))
                eventqueue.eventNr += 1
                self.result.dropped_customers += 1
                self.result.drop_station_dict[station] += 1
                # Ausgabe
                print(str(event[0]) + ":" + self.name + " Dropped at " + station.name)
            else:                               # In Warteschlange einreihen
                station.arrival(self)
                # Ausgabe
                print(str(event[0]) + ":" + self.name + " Queueing at " + station.name)

    def leave(self, eventqueue, event):
        stationWithType = self.stationsWithType.pop()
        station = stationWithType[0]

        station.leave(self)
        # Ausgabe
        print(str(event[0]) + ":" + self.name + " Finished at " + station.name)

        # Ereignis Ankunft an nächster Station erzeugen
        if len(self.stationsWithType) != 0:
            eventtime = event[0]+self.stationsWithType[len(self.stationsWithType) - 1][1][0]    # aktuelle zeit + zeit bis zur nächsten station
            eventqueue.push((eventtime, 1, eventqueue.eventNr, self.arrival))
            eventqueue.eventNr += 1
        else:
            self.result.mediator_period_list.append(event[0] - self.start_time)

        # Falls Kunden in Schlange -> nächsten Kunde aus Warteschlange holen und Ereignis verlassen der Station erzeugen
        if len(station.queue) != 0:
            customer = station.queue[0]

            stationWithType = customer.stationsWithType[len(customer.stationsWithType) - 1]
            station = stationWithType[0]
            type = stationWithType[1]
            eventtime = event[0] + station.duration * type[1]

            eventqueue.push((eventtime, 0, eventqueue.eventNr, customer.leave))
            eventqueue.eventNr += 1

        return self
