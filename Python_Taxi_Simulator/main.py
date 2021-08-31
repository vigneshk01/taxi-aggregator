import sched
import time
from model import RandomTaxiGenerateModel, Taxi, KinesisPublishAndMovement
from schedule import every, repeat, run_pending, clear

file = 'Movement_Location_History_Json/taxi_location_history.json'


def log_time():
    print('---------------------------')
    struct_time = time.localtime()  # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", struct_time)
    print(time_string)


def clear_taxi_movement():
    print('-----------------')
    print('First Clearing taxi_movement job..')
    clear('taxi_movement')
    print('Job cleared')


@repeat(every(6).hours)
def case_taxi_generator(once_only=False):
    if not once_only:
        clear_taxi_movement()

    print('-----------------')
    print('Start taxi random allocation and movement')
    taxi = Taxi()
    taxi.get_taxis()
    print(taxi.taxis)
    random_taxi = RandomTaxiGenerateModel()
    random_taxi.get_data_random_location()
    random_taxi.generate_random_location_for_taxi(taxi.taxis)
    generate_movement(taxi, random_taxi)


def move_taxi(kwargs):
    log_time()
    movement = KinesisPublishAndMovement()
    movement.read_recent_location()
    print(f'Taxi movement start')
    for taxi in kwargs['all_taxi']:
        old_long_lat = movement.get_recent_long_lat_by_taxi_id(taxi['TaxiID'])
        if len(old_long_lat) != 0:
            new_long_lat = movement.calculate_movement(old_long_lat[0], old_long_lat[1])
            check_within_boundary = movement.check_point_in_boundary(
                new_long_lat[0], new_long_lat[1], kwargs['boundary']
            )
            if check_within_boundary:
                new_data = movement.stream_template_data(
                    taxi['TaxiID'], new_long_lat[0], new_long_lat[1], taxi['taxi_type']
                )
            else:
                long_lat_data = movement.choose_random_from_list(kwargs['location_list'])
                new_data = movement.stream_template_data(
                    taxi['TaxiID'], long_lat_data[0], long_lat_data[1], taxi['taxi_type']
                )
            movement.update_location(taxi['TaxiID'], new_data)
        else:
            print(f'No long lat found for taxi with id - {taxi["TaxiID"]}')
    movement.update_all_location_to_json()
    print('Taxi movement finish')


def generate_movement(taxi_object, random_taxi_object):
    all_taxi = taxi_object.taxis
    random_taxi_object.get_boundary()
    dict_to_used = {
        'all_taxi': all_taxi,
        'boundary': random_taxi_object.extract_location(),
        'location_list': random_taxi_object.location_list
    }
    every(1).minutes.do(move_taxi, dict_to_used).tag('taxi_movement').run()


# Driver program
if __name__ == "__main__":
    case_taxi_generator(True)
    while True:
        try:
            run_pending()
        except KeyboardInterrupt:
            break
