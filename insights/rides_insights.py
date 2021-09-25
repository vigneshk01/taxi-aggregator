import numpy  as np
import pandas as pd
import random
import datetime
from bokeh.io import show, output_file
from bokeh.plotting import figure, ColumnDataSource
from bokeh.tile_providers import get_provider, Vendors
from sklearn.cluster import DBSCAN

from database import Database

RIDE_COLLECTION = 'rides'
BOOKING_COLLECTION = 'booking'
LOCATION_STREAM_COLLECTION = 'location_stream'
# If LOCATION_STREAM_COLLECTION is filled properly then taxi routes cane also be drawn on the map
USE_LOCATION = 1
FROM_DATE = '2021-08-01T00:00:00.000'
TO_DATE = '2021-08-31T23:59:59.000'

class gen_map:
    def __init__(self, COLLECTION, from_date, to_date):
        self._db = Database()
        self.df = pd.DataFrame()
        self.dest_cluster_center = []
        self.dest_cluster_radius = []
        self.src_cluster_center = []
        self.src_cluster_radius = []
        self.gen_data(COLLECTION, from_date, to_date)
        # 1200 - No of days 1
        # 500 - No of days 31
        eps = (((500 - 1200) / (7500 - 250)) * (len(self.df.index) - 250)) + 1200
        self.gen_cluster(eps)

    def mercator_coord(self, x, y):
        r_major = 6378137.000
        a = r_major * np.radians(y)
        scale = a/y
        b = 180.0/np.pi * np.log(np.tan(np.pi/4.0 + x * (np.pi/180.0)/2.0)) * scale
        return(a, b)

    def calc_cluster(self, arr_x, arr_y, ep):
        coords = np.array(list((x,y) for x,y in zip(arr_x, arr_y)))
        cluster_points = []
        cluster_center = []
        cluster_radius = []
        dbscan = DBSCAN(eps=ep, min_samples=10).fit(coords)
        core_samples_mask = np.zeros_like(dbscan.labels_, dtype=bool)
        core_samples_mask[dbscan.core_sample_indices_] = True
        labels = dbscan.labels_
        unique_labels = set(labels)
        for k in unique_labels:
            class_member_mask = (labels == k)
            if k != -1:
                xy = coords[class_member_mask & core_samples_mask]
                cluster_points.append(xy)

        for points in cluster_points:
            x = [p[0] for p in points]
            y = [p[1] for p in points]
            centroid = (sum(x) / len(points), sum(y) / len(points))
            cluster_center.append(centroid)
            rad = 0
            for i in range(len(x)):
                dist = (abs(x[i]-centroid[0])**2 + abs(y[i]-centroid[1])**2)**0.5
                if dist > rad:
                    rad = dist
            cluster_radius.append(rad)
        return cluster_center, cluster_radius

    def gen_data(self, collection, from_date, to_date):
        data = self._db.get_all_data(collection, {'booked_time': {'$gte': from_date, '$lt': to_date}})
        entries = list(data)
        df = pd.DataFrame(entries)
        df['passenger_id'] = list(str(y) for y in df['passenger_id'])
        df['_id'] = list(str(y) for y in df['_id'])

        x = df['start_loc']
        df['src_coordinates'] = [self.mercator_coord(y['coordinates'][0], y['coordinates'][1]) for y in x]
        df[['mercator_s_x', 'mercator_s_y']] = df['src_coordinates'].apply(pd.Series)
        x = df['dest_loc']
        df['dest_coordinates'] = [self.mercator_coord(y['coordinates'][0], y['coordinates'][1]) for y in x]
        df[['mercator_d_x', 'mercator_d_y']] = df['dest_coordinates'].apply(pd.Series)
        self.df = df

    def gen_routes(self):
        df = self.df
        coll_x = []
        coll_y = []
        i = 0
        for row in df.iterrows():
            data = self._db.get_single_data(LOCATION_STREAM_COLLECTION, {'ride_id': row[1]['_id']}, {'_id': 0, 'current_loc': 1})
            list_x = []
            list_y = []
            for x in data['current_loc']['coordinates']:
                mer_x, mer_y = self.mercator_coord(x[1],x[0])
                list_x.append(mer_x)
                list_y.append(mer_y)
            coll_x.append(list_x)
            coll_y.append(list_y)

        df['route_x'] = coll_x
        df['route_y'] = coll_y
        self.df = df

    def gen_cluster(self, eps):
        self.src_cluster_center, self.src_cluster_radius = self.calc_cluster(self.df['mercator_s_x'], self.df['mercator_s_y'], eps)
        self.dest_cluster_center, self.dest_cluster_radius = self.calc_cluster(self.df['mercator_d_x'], self.df['mercator_d_y'], eps)

    def gen_map(self, map_name, dfx, use_lines):
        output_file(map_name)
        chosentile = get_provider(Vendors.STAMEN_TONER)
        
        # With tooltips
        # tooltips = [("Passenger","@passenger_id"), ("vehicle_type","@vehicle_type")]
        # p = figure(title = 'Passenger Location', x_axis_type="mercator", y_axis_type="mercator", x_axis_label = 'Longitude', y_axis_label = 'Latitude', tooltips = tooltips)
        
        # Without tooltips
        p = figure(title = 'Passenger Location', x_axis_type="mercator", y_axis_type="mercator", x_axis_label = 'Longitude', y_axis_label = 'Latitude')
        p.add_tile(chosentile)

        sources = [ColumnDataSource(data=x) for x in dfx]
        for source in sources:
            r = random.randint(0,255)
            g = random.randint(0,255)
            b = random.randint(0,255)
            rgb = (r,g,b)

            # FIGURE
            p.circle(x = 'mercator_s_x', y = 'mercator_s_y', fill_color = rgb, source=source, size=5, fill_alpha = 0.7, legend_label='source')
            p.triangle(x = 'mercator_d_x', y = 'mercator_d_y', fill_color = rgb, source=source, size=5, fill_alpha = 0.7, legend_label='destination') 
            if use_lines:
                p.multi_line(xs = 'route_x', ys = 'route_y', line_color= rgb, source=source, line_width=2, line_alpha= 0.3, legend_label='route')

        p.circle(x = list(zip(*self.dest_cluster_center))[0], y = list(zip(*self.dest_cluster_center))[1], radius=self.dest_cluster_radius, fill_color = 'red', fill_alpha= 0.3, legend_label='destination_cluster')
        p.circle(x = list(zip(*self.src_cluster_center))[0], y = list(zip(*self.src_cluster_center))[1], radius=self.src_cluster_radius, fill_color = 'blue', fill_alpha= 0.3, legend_label='source_cluster')
        p.legend.location = "top_left"
        p.legend.click_policy="hide"
        show(p)

    def gen_single_map(self, map_name, dfs, use_lines):
        output_file(map_name)
        chosentile = get_provider(Vendors.STAMEN_TONER)
        
        # With tooltips
        # tooltips = [("Passenger","@passenger_id"), ("vehicle_type","@vehicle_type")]
        # p = figure(title = 'Passenger Location', x_axis_type="mercator", y_axis_type="mercator", x_axis_label = 'Longitude', y_axis_label = 'Latitude', tooltips = tooltips)
        
        # Without tooltips
        p = figure(title = 'Passenger Location', x_axis_type="mercator", y_axis_type="mercator", x_axis_label = 'Longitude', y_axis_label = 'Latitude')
        p.add_tile(chosentile)

        source = ColumnDataSource(data=dfs)
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        rgb = (r,g,b)

        # FIGURE
        p.circle(x = 'mercator_s_x', y = 'mercator_s_y', fill_color = rgb, source=source, size=5, fill_alpha = 0.7, legend_label='source')
        p.triangle(x = 'mercator_d_x', y = 'mercator_d_y', fill_color = rgb, source=source, size=5, fill_alpha = 0.7, legend_label='destination') 
        if use_lines:
            p.multi_line(xs = 'route_x', ys = 'route_y', line_color= rgb, source=source, line_width=2, line_alpha= 0.3, legend_label='route')

        p.circle(x = list(zip(*self.dest_cluster_center))[0], y = list(zip(*self.dest_cluster_center))[1], radius=self.dest_cluster_radius, fill_color = 'red', fill_alpha= 0.3, legend_label='destination_cluster')
        p.circle(x = list(zip(*self.src_cluster_center))[0], y = list(zip(*self.src_cluster_center))[1], radius=self.src_cluster_radius, fill_color = 'blue', fill_alpha= 0.3, legend_label='source_cluster')
        p.legend.location = "top_left"
        p.legend.click_policy="hide"
        show(p)

    def gen_aggr_passenger_id(self):
        dfs = self.df.groupby(self.df.passenger_id)
        dfx = [dfs.get_group(x) for x in dfs.indices]
        return dfx

if __name__ == "__main__":
    now = datetime.datetime.now()

    book = gen_map(BOOKING_COLLECTION, FROM_DATE, TO_DATE)
    book_dfx = book.gen_aggr_passenger_id()
    map_name = 'book-' + now.strftime("%Y-%m-%d-%H-%M-%S") + '.html'
    book.gen_map(map_name, book_dfx, False)
    
    dfs = book.df.groupby(book.df.server_message)
    book.df = dfs.get_group('no cabs available')
    eps = (((500 - 1200) / (7500 - 250)) * (len(book.df.index) - 250)) + 1200
    book.gen_cluster(eps)
    map_name = 'book-failed-booking-' + now.strftime("%Y-%m-%d-%H-%M-%S") + '.html'
    book.gen_single_map(map_name,  book.df, False)

    ride = gen_map(RIDE_COLLECTION, FROM_DATE, TO_DATE)
    if USE_LOCATION:
        ride.gen_routes()
    ride_dfx = ride.gen_aggr_passenger_id()
    map_name = 'ride-' + now.strftime("%Y-%m-%d-%H-%M-%S") + '.html'
    ride.gen_map(map_name, ride_dfx, USE_LOCATION)
