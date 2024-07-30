from pytest import fixture
from fetch_cities_lat_long import create_cities_dataframe, tsp

@fixture
def cities():
    return create_cities_dataframe()


def test_tsp(cities):
    total_distance, df_shortest = tsp(cities)
    assert total_distance < 1000000