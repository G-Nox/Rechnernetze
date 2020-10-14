class Result:
    def __init__(self, drop_station_dict):
        self.count_customers = 0
        self.dropped_customers = 0
        self.simu_end_time = 0
        self.mediator_period_list = []
        self.drop_station_dict = drop_station_dict
