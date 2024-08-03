import time
import os


from akiya_scrapper.utils import dict_csv_list
from akiya_scrapper.config import akiya_config
from akiya_scrapper.utils import CSVHandler, DataFetcher, LoginHandler, setup_logger

logger = setup_logger(__name__, log_file="akiya_scrapper/logs/akiya.log")


class AkiyaScraper:
    def __init__(
        self,
        filename: str,
        path: str,
        login_handler: LoginHandler,
        data_fetcher: DataFetcher,
        csv_handler: CSVHandler,
    ):
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
        total = len(coord_list)
        current = 1
        last_log_time = time.time()
        surplus_coords = []
        logger.info("Starting to scrape data")
        for coord in coord_list:
            base_url = self.api.format(
                coord.get("ne_lon"),
                coord.get("ne_lat"),
                coord.get("sw_lon"),
                coord.get("sw_lat"),
            )

            city = coord.get("city")
            response = self.data_fetcher.get_data(base_url)
            results = response.get("results")
            count = results.get("count")
            if count > 350:
                coord["count"] = count
                logger.info(f"{coord} is over 350 in {city}")
                surplus_coords.append(coord)

            listings = results.get("listings")
            for listing in listings:
                row = dict_csv_list(listing, akiya_config.listings_attributes)
                csv_list.append(row)
            # Append to CSV file
            self.csv_handler.append_to_csv(
                csv_list[1:], output_filepath
            )  # Skip the header row for appending
            csv_list = [akiya_config.listings_attributes]
            # Log percentage progress every 1 minute
            if time.time() - last_log_time >= 60:
                percentage_complete = (current / total) * 100
                logger.info(f"Progress: {percentage_complete:.2f}% complete...")
                last_log_time = time.time()

            current += 1
            time.sleep(1.5)

        new_coords = akiya_config.coordinate_attributes
        new_coords.append("count")
        new_coords_list = [new_coords]
        if surplus_coords:
            for coords in surplus_coords:
                row = dict_csv_list(coords, new_coords)
                new_coords_list.append(row)

        self.csv_handler.write_to_csv(
            new_coords_list, os.path.join(parent_dir, "surplus.csv")
        )
        data = self.csv_handler.read_csv_to_list(output_filepath)
        logger.info(f"Total Current Listings: {len(data)}")
        listing_ids = [int(d["listing_id"]) for d in data]
        logger.info(f"Total Listing IDS: {len(listing_ids)}")
        unique_listing_ids = list(set(listing_ids))
        logger.info(f"Total Unique Listing IDs: {len(unique_listing_ids)}")
        unique_lisings = self.csv_handler.remove_duplicates(data, "listing_id")
        csv_list = [akiya_config.listings_attributes]
        for ul in unique_lisings:
            row = dict_csv_list(ul, akiya_config.listings_attributes)
            csv_list.append(row)
        self.csv_handler.write_to_csv(csv_list, output_filepath)
