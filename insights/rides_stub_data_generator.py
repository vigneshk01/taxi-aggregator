import datetime
import random
import string
from bson import ObjectId
from database import Database

passenger_rating_lst = ["1:Poor Ride", "2:Below Average Ride", "3:Decent Ride", "4:Good Ride", "5:Awesome Ride"]


class MyRide:
    def __init__(self):
        self.vehicle_nums = self.generate_vehicle_details()
        self._db = Database()
        self.dummy = {}

    @staticmethod
    def get_oid():
        oid = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
        return oid

    @staticmethod
    def get_vehicle_type():
        taxi_type = ["UTILITY", "DELUXE", "LUXURY"]
        t_type = random.choices(taxi_type, weights=[40, 60, 100], k=1)
        random_type = t_type[0]
        # print(random_type)
        return random_type

    def generate_vehicle_details(self):
        district = random.sample(range(10, 99), k=10)
        unique_num = random.sample(range(1000, 9999), k=10)
        rto = random.sample(string.ascii_uppercase, k=10)

        vehicle_list = []
        for i in range(0, 10):
            vehicle_list.append(
                "KA" + str(district[i]) + "" + str(rto[i]) + "" + str(unique_num[i]) + ":" + self.get_vehicle_type())
        return vehicle_list

    def randomize_vehicles(self, count=10):
        all_vehicles = self.vehicle_nums
        op = random.choices(all_vehicles, k=count)
        return op

    @staticmethod
    def get_cost():
        price = random.sample(range(10, 100), k=1)
        return price[0]

    @staticmethod
    def get_random_number(st, ed):
        op = random.randint(st, ed)
        return op

    def get_time_details(self, dt, hr):
        time_dict = {}
        timestamp = dt + datetime.timedelta(hours=hr)
        curr_min = self.get_random_number(00, 60)
        time_dict["booked_time"] = timestamp + datetime.timedelta(minutes=curr_min)
        random_ride_start = self.get_random_number(5, 20)
        time_dict["start_time"] = time_dict["booked_time"] + datetime.timedelta(minutes=random_ride_start)
        random_ride_end = self.get_random_number(00, 60)
        time_dict["end_time"] = time_dict["start_time"] + datetime.timedelta(minutes=random_ride_end)
        return time_dict

    @staticmethod
    def get_passenger_ratings():
        passenger_ratings = {}
        rating_lst = passenger_rating_lst
        random_rating = random.choices(rating_lst, cum_weights=[40, 45, 50, 55, 100], k=1)
        idx = random_rating[0]
        op = idx.split(':')
        passenger_ratings["rating"] = op[0]
        passenger_ratings["comment"] = op[1]
        return passenger_ratings

    @staticmethod
    def get_location_details():
        lat_longs = [(12.9035, 77.4914), (12.8546, 77.5676), (12.9872, 77.5197), (13.1002, 77.5995),
                     (13.0276, 77.6339), (12.9976, 77.6129),
                     (12.9212, 77.6203), (12.9619, 77.5990)]

        loc_list = random.choices(lat_longs, cum_weights=[1, 2, 5, 8, 11, 17, 23, 29], k=2)
        return loc_list

    def insert_data_to_db(self, content=None):
        if content is None:
            content = {}
        self._db.insert_single_data('rides', content)


if __name__ == "__main__":
    ride = MyRide()
    start = datetime.datetime.strptime("01-09-2021", "%d-%m-%Y")
    end = datetime.datetime.strptime("30-09-2021", "%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]

    for date in date_generated:

        vehicle_nums = ride.randomize_vehicles(10)
        for vehicle in vehicle_nums:
            hrs_list = random.sample(range(6, 18), k=3)
            for hour in hrs_list:
                passenger_id = ObjectId()

                location_list = ride.get_location_details()
                start_location = location_list[0]
                end_location = location_list[1]

                gen_time = ride.get_time_details(date, hour)

                booked_time = datetime.datetime.strftime(gen_time["booked_time"], '%Y-%m-%dT%H:%M:%S.%f')[:-3]
                start_time = datetime.datetime.strftime(gen_time["start_time"], '%Y-%m-%dT%H:%M:%S.%f')[:-3]
                end_time = datetime.datetime.strftime(gen_time["end_time"], '%Y-%m-%dT%H:%M:%S.%f')[:-3]

                vehicle_num = vehicle.split(':')[0]
                vehicle_type = vehicle.split(':')[1]

                cost = ride.get_cost()

                resp = ride.get_passenger_ratings()
                rating = resp["rating"]
                comment = resp["comment"]

                print(f'{start_location}, \n{end_location}, \n{passenger_id}, \n{booked_time}, \n{start_time},'
                      f' \n{end_time}, \n{vehicle_type}, \n{vehicle_num}, \n{cost}, \n{rating}, \n{comment} ')

                query = {'passenger_id': passenger_id,
                         'start_loc': {'type': "Point", "coordinates": start_location},
                         'dest_loc': {"type": "Point", "coordinates": start_location}, 'booked_time': booked_time,
                         'start_time': start_time, 'end_time': end_time, 'vehicle_type': vehicle_type,
                         'vehicle_num': vehicle_num, 'cost': cost, 'passenger_rating': rating,
                         'passenger_comments': comment}

                ride.insert_data_to_db(query)
