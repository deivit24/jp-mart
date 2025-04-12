import time
import os


from akiya_scrapper.config import akiya_config, CityCoords, Coords
from akiya_scrapper.utils import (
    divide_rectangle,
    dict_csv_list,
    setup_logger,
    count_mapping,
)

logger = setup_logger(__file__)


class CityCoord:
    def __init__(self, login_handler, data_fetcher,city):
        self.api = "https://www.akiya-mart.com/search/geocode?query={}"
        self.coord_api = "https://www.akiya-mart.com/listings/paginate?house=true&condo=true&featured=false&page=0&currency=usd&neLon={}&neLat={}&swLon={}&swLat={}&isMetric=false&parkingOnly=false&sortBy=POPULAR"
        self.login_handler = login_handler
        self.data_fetcher = data_fetcher
        self.coords = CityCoords()
        self.city = city

    def scrape(self) -> CityCoords:
        self.login_handler.login()
        japanese_cities = akiya_config.cities

        logger.info(
            f"Getting coordinates of {self.city} of {len(japanese_cities.cities)} cities in Japan"
        )

        base_url = self.api.format(self.city)
        result = self.data_fetcher.get_data(base_url)
        coord = result["results"]
        north_east = coord.get("north_east")
        south_west = coord.get("south_west")
        time.sleep(1.5)
        base_cord_url = self.coord_api.format(
            north_east.get("lon"),
            north_east.get("lat"),
            south_west.get("lon"),
            south_west.get("lat"),
        )
        count_result = self.data_fetcher.get_data(base_cord_url)
        results = count_result.get("results")
        city_count = results.get("count")
        coord_num = count_mapping(int(city_count))

        rect = divide_rectangle(
            north_east.get("lon"),
            north_east.get("lat"),
            south_west.get("lon"),
            south_west.get("lat"),
            coord_num,
        )
        logger.info(
            f"Splitting coordinates into {coord_num * coord_num} sections for {self.city}"
        )
        self.coords.city = self.city
        self.coords.city_count = city_count
        for rec in rect:
            city_coord = Coords(
                sw_lon=rec.get("sw_lon"),
                sw_lat=rec.get("sw_lat"),
                ne_lat=rec.get("ne_lat"),
                ne_lon=rec.get("ne_lon"),
            )
            self.coords.city_coords.append(city_coord)

        time.sleep(2)

        return self.coords
