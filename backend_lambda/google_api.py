import logging
import time
import googlemaps
import polyline


class Gapi:
    API_Key = '<API_Key>'

    def __init__(self):
        self._gmaps_client = googlemaps.Client(key=Gapi.API_Key)

    def invoke_directions_api(self, origin, destination):
        # directions_result = gmaps.directions("Sydney Town Hall", "Parramatta, NSW", mode="transit",
        # departure_time=now)
        directions_result = self._gmaps_client.directions(origin=origin, destination=destination, mode='driving',
                                                          units='metric')
        return directions_result

    def invoke_geocode_Api(self, address):
        geocode_result = self._gmaps_client.geocode(address)
        return geocode_result

    def invoke_reverse_geocode_api(self, coordinates: tuple):
        reverse_geocode_result = self._gmaps_client.reverse_geocode(coordinates)
        return reverse_geocode_result

    def process_directions_and_movement(self, origin, destination):
        route_list = self.invoke_directions_api(origin, destination)
        steps = route_list[0]['legs'][0]['steps']

        start = time.time()
        for step in steps:

            duration = step["duration"]['value']
            poly_line = step["polyline"]['points']

            points = polyline.decode(poly_line)
            points_per_sec = int(duration) / len(points)

            for point in points:
                time.sleep(points_per_sec)
                logging.debug("%s - %s" % (point, points_per_sec))
                print(point, points_per_sec)

        end = time.time()
        logging.debug('start_time: %s,end_time:%s,total_time: %s' % (start, end, end - start))
        print(f'start_time: {start},end_time: {end},total_time: {end - start}')

# gapi = Gapi()
# gapi.process_directions_and_movement(origin, destination)

# (40.714224, -73.961452) 'madiwalay, Bangalore, CA'
# origin='12.93805958514933, 77.74678327286918',
# destination='12.969351148556541, 77.75000853390684',  mode='driving', units='metric' Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA') Look up an address with reverse
# geocoding
#

# Request directions via public transit
