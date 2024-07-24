#!/usr/bin/env python

"""

This is command-line tool that figures out the shortest distance to visit all cities in the list. 

"""

import geopy
import geopy.distance
import pandas as pd
from random import shuffle 
import click 

#build a function that takes variable length argument of strings and returns a list of cities 
def my_cities(*args):
    return list(args)

def create_cities_dataframe(cities=None):

    if cities is None:
        cities = [
            "New York",
            "Tokyo",
            "London",
            "Paris",
            "Sydney",
            "Toronto",
            "Dubai",
            "Berlin",
            "Singapore",
            "Hong Kong"
        ]

    latitudes = []
    longitudes = []

    for city in cities:
        geolocator = geopy.geocoders.Nominatim(user_agent="tsp_pandas")
        location = geolocator.geocode(city)
        latitudes.append(location.latitude)
        longitudes.append(location.longitude)
        
    df = pd.DataFrame(
        {
            "city": cities,
            "latitude": latitudes,
            "longitude": longitudes
        }
    )

    return df


def tsp(city_df):

    city_list = city_df['city'].to_list()

    shuffle(city_list)

    print(f"Randomized city list: {city_list}")

    distance_list = []

    for i in range(len(city_list)):

        if i != len(city_list):

            distance = geopy.distance.distance(
                (
                    city_df[city_df["city"] == city_list[i]]['latitude'].values[0],
                    city_df[city_df["city"] == city_list[i]]['longitude'].values[0]
                ),
                (
                    city_df[city_df["city"] == city_list[i+1]]['latitude'].values[0],
                    city_df[city_df["city"] == city_list[i+1]]['longitude'].values[0]
                )
            ).miles 

            distance_list.append(distance)

        
        total_distance = sum(distance_list)

        return total_distance, city_list


def main(count):
    """ Main function that runs the tsp simulation multiple times """
    distance_list = []
    city_list_list= []

    cdf = create_cities_dataframe()

    # loop through the similation

    for i in range(count):

        distance, city_list = tsp(cdf)
        print(f"Running similation {i}: Found total distance: {distance}")

        # append distance to the distance list
        distance_list.append(distance)

        city_list_list.append(city_list)

    shortest_distance_index = distance_list.index(min(distance_list))

    print(f"Shortest distance: {shortest_distance_index}")
    print(f"Cities visited: {city_list_list[shortest_distance_index]}")


@click.group()
def cli():
    """This is a command-line tool that figures out the shortest distance to visit all cities in a list"""

# add click command that runs the simulation x times 
@cli.command("simulate")
@click.option("--count", default=10, help="Number of times to run the simulation.")
def simulate(count):
    """
        Run the simulation x times.

        Example : 

        ./fetch_cities_lat_long simulate --count 15
    """

    print(f"Running simulation {count} times")
    main(count)

if __name__=="__main__":
    cli()

