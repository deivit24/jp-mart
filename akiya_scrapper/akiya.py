import logging
import time
import os


from akiya_scrapper.utils import dict_csv_list
from akiya_scrapper.config import akiya_config

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


class AkiyaScraper:
    def __init__(self, filename, path, login_handler, data_fetcher, csv_handler):
        self.api = "https://www.akiya-mart.com/listings/paginate?house=true&condo=true&featured=false&currency=usd&neLon={}&neLat={}&swLon={}&swLat={}&isMetric=false&parkingOnly=false&sortBy=POPULAR"
        self.filename = filename
        self.path = path
        self.login_handler = login_handler
        self.data_fetcher = data_fetcher
        self.csv_handler = csv_handler

    def scrape(self):
        self.login_handler.login()
        parent_dir = os.path.join(self.path, "csv_files")
        os.makedirs(parent_dir, exist_ok=True)
        coord_filepath = os.path.join(parent_dir, "coordinates.csv")
        output_filepath = os.path.join(parent_dir, self.filename)
        coord_list = self.csv_handler.read_csv_to_list(coord_filepath)
        csv_list = [akiya_config.listings_attributes]

        self.csv_handler.write_to_csv(
            [akiya_config.listings_attributes], output_filepath
        )
        for coord in coord_list:
            base_url = self.api.format(
                coord.get("ne_lon"),
                coord.get("ne_lat"),
                coord.get("sw_lon"),
                coord.get("sw_lat"),
            )

            response = self.data_fetcher.get_data(base_url)
            results = response.get("results")
            count = results.get("count")
            logger.info(f"Count: {count}")
            listings = results.get("listings")
            for listing in listings:
                row = dict_csv_list(listing, akiya_config.listings_attributes)
                csv_list.append(row)
            # Append to CSV file
            self.csv_handler.append_to_csv(
                csv_list[1:], output_filepath
            )  # Skip the header row for appending
            csv_list = [akiya_config.listings_attributes]
            logger.info(f"Successfully wrote to {output_filepath}")
            time.sleep(1.5)
