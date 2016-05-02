#!/usr/bin/python
#
# Travel Time Estimator
# Queries Google Maps API and stores the travel time to a series of desntinations set in the top of this file from
# a single source, saving the results to a log file

import googlemaps
from datetime import datetime
import os
import json

PATH = '/home/ben/traveltime/'

params = json.load(open(PATH + 'params.secret'))

with open(PATH + "key.secret") as fin:
    key = fin.readline()[0:-1]

gmaps = googlemaps.Client(key=key)

res_forward = gmaps.distance_matrix(params['Origins'].keys(), params['Destinations'].keys(), departure_time="now", units="imperial")
res_reverse = gmaps.distance_matrix(params['Destinations'].keys(), params['Origins'].keys(), departure_time="now", units="imperial")
print res_forward

# Output: Datetime, followed by distance, travel time, and travel time with traffic to each destination
out = datetime.now().isoformat(' ') + ','

for i in range(len(params['Destinations'].keys())):
    for j in range(len(params['Origins'].keys())):
        out += '%f,' % (res_forward['rows'][j]['elements'][i]['distance']['value'] * 0.000621371192)
        out += '%f,' % (res_forward['rows'][j]['elements'][i]['duration']['value'] / 60.0)
        out += '%f,' % (res_forward['rows'][j]['elements'][i]['duration_in_traffic']['value'] / 60.0)

for i in range(len(params['Destinations'].keys())):
    for j in range(len(params['Origins'].keys())):
        out += '%f,' % (res_reverse['rows'][i]['elements'][j]['distance']['value'] * 0.000621371192)
        out += '%f,' % (res_reverse['rows'][i]['elements'][j]['duration']['value'] / 60.0)
        out += '%f,' % (res_reverse['rows'][i]['elements'][j]['duration_in_traffic']['value'] / 60.0)

print out

logfile = PATH + 'log.csv'

if not os.path.exists(logfile):
    with open(logfile, 'w') as fout:
        fout.write('Time,')
        for dest in params['Destinations'].values():
            for src in params['Origins'].values():
                fout.write('%s to %s Dist (mi),' % (src, dest))
                fout.write('%s to %s Time (min),' % (src, dest))
                fout.write('%s to %s Time w/ Traffic (min),' % (src, dest))

        for dest in params['Destinations'].values():
            for src in params['Origins'].values():
                fout.write('%s to %s Dist (mi),' % (dest, src))
                fout.write('%s to %s Time (min),' % (dest, src))
                fout.write('%s to %s Time w/ Traffic (min),' % (dest, src))
        fout.write('\n')

with open(logfile, 'a') as fout:
    fout.write(out + '\n')

with open(PATH + 'dump.txt', 'a') as fout:
    fout.write(str(res_forward) + '::::' + str(res_reverse) + '\n')
