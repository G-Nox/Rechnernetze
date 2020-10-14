from collections import deque
from task1_realzeit.Customer import Customer
from task1_realzeit.Station import Station
from task1_realzeit.Result import Result
from threading import Thread
import time


def main():
    baecker = Station('Bäcker', 10)
    wursttheke = Station('Metzger', 30)
    kaesetheke = Station('Käse', 60)
    kasse = Station('Kasse', 5)

    baecker.start()
    wursttheke.start()
    kaesetheke.start()
    kasse.start()

    typ1 = deque([(kasse, (60, 30, 20)), (kaesetheke, (45, 3, 5)), (wursttheke, (30, 5, 10)), (baecker, (10, 10, 10))])
    typ2 = deque([(baecker, (20, 3, 20)), (kasse, (30, 3, 20)), (wursttheke, (30, 2, 5))])

    drop_station_dict = {
        baecker: 0,
        wursttheke: 0,
        kaesetheke: 0,
        kasse: 0
    }
    result = Result(drop_station_dict)

    start_time = time.time()

    baecker.start_time = start_time
    wursttheke.start_time = start_time
    kaesetheke.start_time = start_time
    kasse.start_time = start_time

    start_thread_typ1 = Thread(target=start_typ1, args=(201, typ1, result, start_time))
    start_thread_typ2 = Thread(target=start_typ2, args=(62, typ2, result, start_time))

    start_thread_typ1.start()
    start_thread_typ2.start()

    time.sleep(120)

    # Result-Berechnung
    # mediator_period = 0
    # for time in result.mediator_period_list:
    #     mediator_period += time
    # mediator_period = mediator_period / (len(result.mediator_period_list))

    drop_perc_baecker = result.drop_station_dict[baecker] / result.count_customers * 100
    drop_perc_wurst = result.drop_station_dict[wursttheke] / result.count_customers * 100
    drop_perc_kaese = result.drop_station_dict[kaesetheke] / result.count_customers * 100
    drop_perc_kasse = result.drop_station_dict[kasse] / result.count_customers * 100

    # Result-Ausgabe
    print("Simulationsende: " + str(result.simu_end_time) + 's')
    print("Anzahl Kunden: " + str(result.count_customers))
    print("Anzahl vollständige Einkäufe: " + str(result.count_customers - result.dropped_customers))
 #   print("Mittlere Einkaufsdauer: " + str(mediator_period) + 's')
    print("Drop percentage at Bäcker: " + str(drop_perc_baecker))
    print("Drop percentage at Metzger: " + str(drop_perc_wurst))
    print("Drop percentage at Käse: " + str(drop_perc_kaese))
    print("Drop percentage at Kasse: " + str(drop_perc_kasse))

    print("Ende \n")


def start_typ1(target_time, typ1, result, start_time):
    actual_time = time.time() - start_time
    countA = 1
    sleep_duration = 200

    while actual_time < target_time:
        thread = Customer(typ1.copy(), "A" + str(countA), result, start_time)
        countA += 1
        thread.start()
        time.sleep(sleep_duration)
        actual_time += sleep_duration


def start_typ2(target_time, typ2, result, start_time):
    actual_time = time.time() - start_time
    countB = 1
    sleep_duration = 60

    time.sleep(1)
    while actual_time < target_time:
        thread = Customer(typ2.copy(), "B" + str(countB), result, start_time)
        countB += 1
        thread.start()
        time.sleep(sleep_duration)
        actual_time += sleep_duration


main()
