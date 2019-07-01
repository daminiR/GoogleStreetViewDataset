import geocoder
import argparse
import csv
import google_streetview.api
import datetime
# parse the county list and no need to format yet only when creating heat map
import tqdm
from operator import attrgetter
now = datetime.datetime.now()
from statistics import mean
city_state_list = set()
with open('us_cities_states_counties.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter="|")
    for row in csv_reader:
        try:
            querry = row[0] + ', ' + row[1]
            city_state_list.add(querry)
        except:
            pass

with open("update_result.csv", "w") as csvfile:
    filewriter = csv.writer(csvfile, delimiter=",",  quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(["City", "State", "County", "lat", "lng", "street_view_update"])
    latlng_list = list()
    for query in city_state_list:
        time_list = list()
        g = geocoder.arcgis(query, maxRows=5)
        for result in g:
                print(result.address)
                city, state = query.split(",")
                filewriter.writerow([city, state, result.latlng[0], result.latlng[1]])
                latlng_list.append(result.latlng)

        break
    google_query = str(latlng_list).replace('],', ";")
    google_query = google_query.replace('[', '')
    print(google_query)

    apiargs = {
        'location': google_query,
        'key': 'AIzaSyDeXJJgleZMO-edNOq7mNzDpa1ei1KHwPA'
    }
    api_list = google_streetview.helpers.api_list(apiargs)

    results = google_streetview.api.results(api_list)
    print(len(results.metadata))
    for no_street in range(len(results.metadata)):
        try:
                year, month = results.metadata[no_street]["date"].split('-')
                print(year, month)
                update_months_street_image = int(year) * 12 + int(month)
                time_since =(now.year * 12 + now.month) - update_months_street_image
                time_list.append(time_since)
                print(time_list)
        except:
            pass
        else:
            city_avg_update = mean(time_list)
            print(city_avg_update)
        filewriter.writerow([city, state, result.latlng[0], result.latlng[1]])

    results.save_metadata('metadata.json')