import csv
import geocoder
import requests
import json
reader = csv.reader(open('saved.csv', 'r'))
next(reader)
next(reader)

with open("saved3.csv", "w+") as csvfile:
    filewriter = csv.writer(csvfile, delimiter=",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(["City", "count",  "State", "County", "lat", "lng", "street_view_update"])
    city_data_url = 'http://api.sba.gov/geodata/primary_links_for_city_of/%s/%s.json'
    reader_county = csv.reader(open('us_cities_states_counties.csv', 'r'))
    next(reader_county)
    for row in reader:
        print(row)
        try :
            state = row[1]
            state = state.strip()
            city = row[0]
            city = city.replace("\n", "")
            lat = row[2]
            lng = row[3]
            months = row[4]
            # print("this is city = {}".format(city)      )
            print(state)
            # print(len(state))
            for row2 in reader_county:
                # print(row2)
                # print(row2)
                try:
                    county = row2[0].split("|")[3]
                except:
                    pass
                CITY_2 = row2[0].split("|")[0]
                CITY_2 =  CITY_2.replace("\n", "")
                State2 =  row2[0].split("|")[1]
                if (city == CITY_2) and (len(city) == len(CITY_2)) and (state == State2) :
                    filewriter.writerow([city, county, state, lat, lng, months ])
                    print(county)
        except:
            pass
