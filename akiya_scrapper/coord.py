import logging
import time
import os


from akiya_scrapper.config import akiya_config
from akiya_scrapper.utils import flatten_dict, divide_rectangle, dict_csv_list

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


class CityCoord:
    def __init__(self, path, login_handler, data_fetcher, csv_handler):
        self.api = "https://www.akiya-mart.com/search/geocode?query={}"
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
            rect = divide_rectangle(
                north_east.get("lon"),
                north_east.get("lat"),
                south_west.get("lon"),
                south_west.get("lat"),
                city.num,
            )
            logger.info(
                f"Splitting coordinates into {city.num} sections for {city.name}"
            )
            for rec in rect:
                rec["city"] = city.name
                row = dict_csv_list(rec, akiya_config.coordinate_attributes)
                csv_list.append(row)

            time.sleep(2)

        self.csv_handler.write_to_csv(csv_list, csv_filepath)
