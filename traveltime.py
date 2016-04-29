#!/usr/bin/python
#
# Travel Time Estimator
# Queries Google Maps API and stores the travel time to a series of desntinations set in the top of this file from
# a single source, saving the results to a log file

import googlemaps
from datetime import datetime
import os
import json

params = json.load(open('params.secret'))

with open("key.secret") as fin:
    key = fin.readline()

gmaps = googlemaps.Client(key=key)

result = gmaps.distance_matrix(params['Origin'], params['Destinations'].keys(), departure_time="now", units="imperial")
print result

# Output: Datetime, followed by distance, travel time, and travel time with traffic to each destination
out = datetime.now().isoformat(' ') + ','

for i in range(len(params['Destinations'].keys())):
    out += '%f,' % (result['rows'][0]['elements'][i]['distance']['value'] * 0.000621371192)
    out += '%f,' % (result['rows'][0]['elements'][i]['duration']['value'] / 60.0)
    out += '%f,' % (result['rows'][0]['elements'][i]['duration_in_traffic']['value'] / 60.0)

print out

if not os.path.exists('log.csv'):
    with open('log.csv', 'w') as fout:
        fout.write('Time,')
        for item in params['Destinations'].values():
            fout.write(item + ' Dist (mi),')
            fout.write(item + ' Time (min),')
            fout.write(item + ' Time w/ Traffic (min),')
        fout.write('\n')

with open('log.csv', 'a') as fout:
    fout.write(out + '\n')
