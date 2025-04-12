import time
import os


from akiya_scrapper.utils import dict_csv_list
from akiya_scrapper.config import akiya_config, COORDIATE_ATTRIBUTES, CityCoords
from akiya_scrapper.utils import CSVHandler, DataFetcher, LoginHandler, setup_logger

logger = setup_logger(__name__, log_file="akiya_scrapper/logs/akiya.log")


class AkiyaScraper:
    def __init__(
        self,
        filename: str,
        path: str,
        city_coords: CityCoords,
        login_handler: LoginHandler,
        data_fetcher: DataFetcher,
        csv_handler: CSVHandler,
    ):
        self.api = "https://www.akiya-mart.com/listings/paginate?condo={}&house={}&featured=false&isSold=false&currency=usd&neLon={}&neLat={}&swLon={}&swLat={}&isMetric=false&parkingOnly=false&sortBy=POPULAR"
        self.filename = filename
        self.path = path
        self.city_coords = city_coords
        self.login_handler = login_handler
        self.data_fetcher = data_fetcher
        self.csv_handler = csv_handler
        self.akiya_types = [
            {
                "type": "house",
                "is_house": "true",
                "is_condo": "false",
            },
            {
                "type": "condo",
                "is_house": "false",
                "is_condo": "true",

            }
        ]

    def scrape(self):
        self.login_handler.login()
        os.makedirs(self.path, exist_ok=True)
        output_filepath = os.path.join(self.path, self.filename)
        csv_list = [akiya_config.listings_attributes]

        self.csv_handler.write_to_csv(
            [akiya_config.listings_attributes], output_filepath
        )
        # we are multiplying by two since we are going to loop through them twice
        total = len(self.city_coords.city_coords) * 2
        current = 1
        last_log_time = time.time()
        surplus_coords = []
        logger.info("Starting to scrape data")
        for home_type in self.akiya_types:
            akiya_type = home_type.get("type", None)
            is_condo = home_type.get("is_condo", None)
            is_house = home_type.get("is_house", None)
            for coord in self.city_coords.city_coords:
                base_url = self.api.format(
                    is_condo,
                    is_house,
                    coord.ne_lon,
                    coord.ne_lat,
                    coord.sw_lon,
                    coord.sw_lat,
                )

                city = self.city_coords.city
                response = self.data_fetcher.get_data(base_url)
                results = response.get("results")
                count = results.get("count")
                if count > 350:
                    coord_dict = coord.model_dump()
                    coord_dict["count"] = count
                    logger.info(f"{coord} is over 350 in {city}")
                    surplus_coords.append(coord_dict)

                listings = results.get("listings")
                for listing in listings:
                    listing["akiya_type"] = akiya_type
                    listing["city"] = city
                    row = dict_csv_list(listing, akiya_config.listings_attributes)
                    csv_list.append(row)
                # Append to CSV file
                self.csv_handler.append_to_csv(
                    csv_list[1:], output_filepath
                )  # Skip the header row for appending
                csv_list = [akiya_config.listings_attributes]
                # Log percentage progress every 1 minute
                if time.time() - last_log_time >= 10:
                    percentage_complete = (current / total) * 100
                    logger.info(f"Progress: {percentage_complete:.2f}% complete...")
                    last_log_time = time.time()

                current += 1
                time.sleep(1.5)

        new_coords = [*COORDIATE_ATTRIBUTES, "count"]
        new_coords_list = [new_coords]
        if surplus_coords:
            for coords in surplus_coords:
                row = dict_csv_list(coords, new_coords)
                new_coords_list.append(row)

            self.csv_handler.write_to_csv(
                new_coords_list, os.path.join(self.path, "surplus.csv")
            )

        data = self.csv_handler.read_csv_to_list(output_filepath)
        listing_ids = [int(d["listing_id"]) for d in data]
        logger.info(f"Total Listing IDS: {len(listing_ids)}")
        unique_listing_ids = list(set(listing_ids))
        logger.info(f"Total Unique Listing IDs: {len(unique_listing_ids)}")
        unique_listings = self.csv_handler.remove_duplicates(data, "listing_id")
        logger.info(f"Total Unique Listing IDs After Removal: {len(unique_listings)}")
        csv_list = [akiya_config.listings_attributes]
        for ul in unique_listings:
            row = dict_csv_list(ul, akiya_config.listings_attributes)
            csv_list.append(row)
        self.csv_handler.write_to_csv(csv_list, output_filepath)
