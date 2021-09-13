import matplotlib.pyplot as plt
import pandas as pd
from database import Database

db = Database()

curr_date = '2021-09-01T00:00:00.000'
end_date = '2021-09-02T00:00:00.000'

data = db.get_all_data('rides', {'start_time': {'$gte': "2021-09-01T00:00:00.000", '$lt': "2021-09-02T00:00:00.000"}},
                       {'_id': 0, 'start_time': 1, 'start_loc': 1})
lst = list(data)

x = [i["start_loc"]["coordinates"][0] for i in lst]
y = [i["start_loc"]["coordinates"][1] for i in lst]

x_frame = pd.DataFrame(x)
y_frame = pd.DataFrame(y)

map_box = (77.3005, 77.9432, 12.7629, 13.2152)
ruh_m = plt.imread('map.png')

fig, ax = plt.subplots(figsize=(8, 7))
ax.scatter(y, x, zorder=1, alpha=0.2, c='black', s=30)
ax.set_title('Plotting Spatial Data on Bangalore Map')

ax.set_xlim(map_box[0], map_box[1])
ax.set_ylim(map_box[2], map_box[3])
ax.imshow(ruh_m, zorder=0, extent=map_box, aspect='equal')
plt.show()
