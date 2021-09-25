import time
from api import Api
from model import RandomTaxiGenerateModel, Taxi, KinesisPublishAndMovement
from schedule import every, run_pending


def log_time():
    print(f'---------------------------')
    struct_time = time.localtime()  # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", struct_time)
    print(time_string)


class GenerateAndMove:

    def __init__(self, taxi, area_boundary, index):
        self._taxi = [taxi]
        self._taxi_details = taxi
        self._boundary = area_boundary
        self._index = index
        self.generate_and_move()

    def generate_and_move(self):
        random_taxi = RandomTaxiGenerateModel()
        random_taxi.get_data_random_location()
        random_taxi.generate_random_location_for_taxi(self._taxi, self._index)
        dict_to_used = {
            'taxi': self._taxi[0],
            'boundary': self._boundary,
            'location_list': random_taxi.location_list
        }
        # every is schedule method which will simulate movement at every min
        every(1).minutes.do(
            self.move_taxi, dict_to_used
        ).tag(f'taxi_movement_{self._taxi_details["vehicle_num"]}')

    def move_taxi(self, common_dict):
        log_time()
        taxi = common_dict['taxi']
        movement = KinesisPublishAndMovement()
        movement.read_recent_location(taxi['vehicle_num'])
        old_long_lat = movement.get_recent_long_lat_for_taxi_id()
        if len(old_long_lat) != 0:
            new_long_lat = movement.calculate_movement(old_long_lat[0], old_long_lat[1])
            check_within_boundary = movement.check_point_in_boundary(
                new_long_lat[0], new_long_lat[1], common_dict['boundary']
            )
            if check_within_boundary:
                new_data = movement.stream_template_data(taxi, new_long_lat[0], new_long_lat[1])
            else:
                long_lat_data = movement.choose_random_from_list(common_dict['location_list'])
                new_data = movement.stream_template_data(taxi, long_lat_data[0], long_lat_data[1])
            movement.update_location_to_json(taxi['vehicle_num'], new_data)
        else:
            print(f'No long lat found for taxi with id - {taxi["vehicle_num"]}')


def call_api_taxis():
    api = Api()
    taxis = api.get_request('/alltaxis')
    return taxis

def call_api_boundary():
    api = Api()
    boundary = api.get_request('/api/ridesearch/getboundary')
    return boundary


def taxi_generator():
    try:
        taxi_list = call_api_taxis()
        boundary = call_api_boundary()
        if taxi_list and boundary:
            area_boundary = boundary['geometry']['coordinates']
            for index, val in enumerate(taxi_list, start=0):
                GenerateAndMove(val, area_boundary, index)
        else:
            raise TypeError
    except TypeError:
        print('Error in Api')


if __name__ == "__main__":
    taxi_generator()
    while True:
        try:
            run_pending()
        except KeyboardInterrupt:
            break
