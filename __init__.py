from collections import deque
from task1_ereignisorientiert.Customer import Customer
from task1_ereignisorientiert.Station import Station
from task1_ereignisorientiert.Eventqueue import Eventqueue
from task1_ereignisorientiert.Result import Result


def main():
    baecker = Station('Bäcker', 10)
    wursttheke = Station('Metzger', 30)
    kaesetheke = Station('Käse', 60)
    kasse = Station('Kasse', 5)

    typ1 = deque([(kasse, (60, 30, 20)), (kaesetheke, (45, 3, 5)),
                  (wursttheke, (30, 5, 10)), (baecker, (10, 10, 10))])
    typ2 = deque([(baecker, (20, 3, 20)), (kasse, (30, 3, 20)),
                  (wursttheke, (30, 2, 5))])

    drop_station_dict = {
        baecker: 0,
        wursttheke: 0,
        kaesetheke: 0,
        kasse: 0
    }
    result = Result(drop_station_dict)

    eventQueue = initSimulation(1801, typ1, typ2, result)
    result = eventQueue.start()

    # Result-Berechnung
    mediator_period = 0
    for time in result.mediator_period_list:
        mediator_period += time
    mediator_period = mediator_period / (len(result.mediator_period_list))

    drop_perc_baecker = result.drop_station_dict[baecker] / \
        result.count_customers * 100
    drop_perc_wurst = result.drop_station_dict[wursttheke] / \
        result.count_customers * 100
    drop_perc_kaese = result.drop_station_dict[kaesetheke] / \
        result.count_customers * 100
    drop_perc_kasse = result.drop_station_dict[kasse] / \
        result.count_customers * 100

    # Result-Ausgabe
    print("Simulationsende: " + str(result.simu_end_time) + 's')
    print("Anzahl Kunden: " + str(result.count_customers))
    print("Anzahl vollständige Einkäufe: " +
          str(result.count_customers - result.dropped_customers))
    print("Mittlere Einkaufsdauer: " + str(mediator_period) + 's')
    print("Drop percentage at Bäcker: " + str(drop_perc_baecker))
    print("Drop percentage at Metzger: " + str(drop_perc_wurst))
    print("Drop percentage at Käse: " + str(drop_perc_kaese))
    print("Drop percentage at Kasse: " + str(drop_perc_kasse))

    print("Ende \n")


def initSimulation(time, typ1, typ2, result):
    eventHQ = Eventqueue()
    eventNr = 0
    countA = 1
    countB = 1
    for i in range(time):
        if i % 200 == 0:
            eventHQ.push((i, 1, eventNr,  Customer(
                typ1.copy(), "A" + str(countA), result).start))
            eventNr += 1
            countA += 1
        elif i % 60 == 1:
            eventHQ.push((i, 1, eventNr,  Customer(
                typ2.copy(), "B" + str(countB), result).start))
            eventNr += 1
            countB += 1

    eventHQ.eventNr = eventNr
    return eventHQ


# main()
