import time
import os


from akiya_scrapper.config import akiya_config
from akiya_scrapper.utils import (
    divide_rectangle,
    dict_csv_list,
    setup_logger,
    count_mapping,
)

logger = setup_logger(__file__)


class CityCoord:
    def __init__(self, path, login_handler, data_fetcher, csv_handler):
        self.api = "https://www.akiya-mart.com/search/geocode?query={}"
        self.coord_api = "https://www.akiya-mart.com/listings/paginate?house=true&condo=true&featured=false&page=0&currency=usd&neLon={}&neLat={}&swLon={}&swLat={}&isMetric=false&parkingOnly=false&sortBy=POPULAR"
        self.path = path
        self.login_handler = login_handler
        self.data_fetcher = data_fetcher
        self.csv_handler = csv_handler

    def scrape(self):
        self.login_handler.login()
        parent_dir = os.path.join(self.path, "csv_files")
        os.makedirs(parent_dir, exist_ok=True)
        cities = akiya_config.cities
        csv_filepath = os.path.join(parent_dir, "coordinates.csv")
        csv_list = [akiya_config.coordinate_attributes]

        for city in cities:
            logger.info(
                f"Getting coordinates of {city.name} of {len(cities)} cities in Japan"
            )

            base_url = self.api.format(city.name)
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
                f"Splitting coordinates into {coord_num * coord_num} sections for {city.name}"
            )
            for rec in rect:
                rec["city"] = city.name
                rec["city_count"] = city_count
                row = dict_csv_list(rec, akiya_config.coordinate_attributes)
                csv_list.append(row)

            time.sleep(2)

        self.csv_handler.write_to_csv(csv_list, csv_filepath)
