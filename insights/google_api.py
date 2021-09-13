import logging
import time
import googlemaps
import polyline


class Gapi:
    API_Key = 'AIzaSyDyRi7MuGjrLBWt32v_T1U4DEeTAjdjnr8'

    def __init__(self):
        self._gmaps_client = googlemaps.Client(key=Gapi.API_Key, queries_per_second=1)

    def invoke_directions_api(self, origin, destination):
        current_delay = 0.1  # Set the initial retry delay to 100ms.
        max_delay = 5  # Set the maximum retry delay to 5 seconds.
        while True:
            print('while')
            try:
                time.sleep(600)
                print('try')
                directions_result = self._gmaps_client.directions(origin=origin, destination=destination,
                                                                  mode='driving', units='metric')
            except googlemaps.exceptions.Timeout as err:
                print("T%s" % err)
                pass
            except googlemaps.exceptions._OverQueryLimit as err:
                print("O%s" % err)
                pass
            except googlemaps.exceptions.ApiError as err:
                print("A%s" % err)
                pass
            except googlemaps.exceptions.HTTPError as err:
                print("H%s" % err)
                pass
            else:
                # If we didn't get an IOError then parse the result.
                return directions_result

            if current_delay > max_delay:
                raise Exception("Too many retry attempts.")

            print("Waiting", current_delay, "seconds before retrying.")

            time.sleep(current_delay)
            current_delay *= 2

    def invoke_geocode_api(self, address):
        geocode_result = self._gmaps_client.geocode(address)
        return geocode_result

    def invoke_reverse_geocode_api(self, coordinates: tuple):
        reverse_geocode_result = self._gmaps_client.reverse_geocode(coordinates)
        return reverse_geocode_result

    def process_directions_and_movement(self, origin, destination, real=True):
        points_per_sec = None
        route_polyline = []
        route_list = self.invoke_directions_api(origin, destination)
        steps = route_list[0]['legs'][0]['steps']
        avg_time = int(route_list[0]['legs'][0]['duration']['value'])

        start_time = time.time()
        for step in steps:

            duration = step["duration"]['value']
            poly_line = step["polyline"]['points']

            points = polyline.decode(poly_line)
            points_per_sec = int(duration) / len(points)

            for point in points:
                if real:
                    time.sleep(points_per_sec)
                logging.debug("%s - %s" % (point, points_per_sec))
                # print(point, points_per_sec)
                route_polyline.append(point)

        end_time = time.time()
        logging.debug('start_time: %s,end_time:%s,total_time: %s' % (start_time, end_time, end_time - start_time))
        print(f'start_time: {start_time},end_time: {end_time},total_time: {end_time - start_time}')
        # print(route_polyline)
        return avg_time, route_polyline, points_per_sec

# gapi = Gapi()
# start = (12.9212, 77.6203)
# end = (12.9619, 77.5990)
# gapi.process_directions_and_movement(start, end, real=False)
