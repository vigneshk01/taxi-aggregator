import sched
import time
from model import RandomTaxiGenerateModel, Taxi, KinesisPublishAndMovement

file = 'Movement_Location_History_Json/taxi_location_history.json'


def log_time():
    print('---------------------------')
    struct_time = time.localtime()  # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", struct_time)
    print(time_string)

def execute_choice(choice):
    if choice == 1:
        case_taxi_generator()
    elif choice == 2:
        generate_movement()
    else:
        print("Choice is not valid")


def case_taxi_generator():
    taxi = Taxi()
    taxi.get_taxi_ids()
    print(taxi.Taxi_Ids)
    random_taxi = RandomTaxiGenerateModel()
    random_taxi.get_data_random_location()
    random_taxi.generate_random_location_for_taxi(taxi.Taxi_Ids)



def move_taxi(**kwargs):
    log_time()
    movement = KinesisPublishAndMovement()
    movement.read_recent_location()
    print(f'Taxi movement start')
    for taxi_id in kwargs['all_taxi']:
        old_long_lat = movement.get_recent_long_lat_by_taxi_id(taxi_id)
        if len(old_long_lat) != 0:
            new_long_lat = movement.calculate_movement(old_long_lat[0], old_long_lat[1])
            check_within_boundary = movement.check_point_in_boundary(
                new_long_lat[0], new_long_lat[1], kwargs['boundary']
            )
            if check_within_boundary:
                new_data = movement.stream_template_data(taxi_id, new_long_lat[0], new_long_lat[1])
            else:
                long_lat_data = movement.choose_random_from_list(kwargs['location_list'])
                new_data = movement.stream_template_data(taxi_id, long_lat_data[0], long_lat_data[1])
            movement.update_location(taxi_id, new_data)
        else:
            print(f'No long lat found for taxi with id - {taxi_id}')
    movement.update_all_location_to_json()
    print('Taxi movement finish')


def movement_scheduler(common_dict):
    scheduler = sched.scheduler(time.time, time.sleep)
    now = time.time()
    loopcount = 0
    while True:
        try:
            scheduler.enterabs(now + loopcount, 1, move_taxi, kwargs=common_dict)
            loopcount += 60
            scheduler.run()
        except KeyboardInterrupt:
            break
    print("Taxi movement has stopped")


def generate_movement():
    taxi = Taxi()
    taxi.get_taxi_ids()
    all_taxi = taxi.Taxi_Ids
    taxi_data = RandomTaxiGenerateModel()
    taxi_data.get_boundary()
    taxi_data.get_data_random_location()
    dict_to_used = {
        'all_taxi': all_taxi,
        'boundary': taxi_data.extract_location(),
        'location_list': taxi_data.location_list
    }
    movement_scheduler(dict_to_used)


if __name__ == "__main__":
    print('****************************************')
    print('* 1 For Random Taxi generator')
    print('* 2 For Taxi movement')
    print('****************************************')

    choice = int(input('Enter Your Choice: '))
    execute_choice(choice)
