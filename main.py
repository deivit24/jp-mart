import os

import argparse

from datetime import datetime, timezone
from akiya_scrapper.akiya import AkiyaScraper
from akiya_scrapper.coord import CityCoord
from akiya_scrapper.utils import LoginHandler, DataFetcher, CSVHandler
from akiya_scrapper.config import akiya_config


# Get the current date and time for the filename
CURRENT_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

PATH = os.path.dirname(os.path.realpath(__file__))


def main():
    login_handler = LoginHandler(
        email=akiya_config.email, password=akiya_config.password
    )
    data_fetcher = DataFetcher(login_handler.get_session())
    csv_handler = CSVHandler()

    city_coord = CityCoord(
        path=PATH,
        login_handler=login_handler,
        data_fetcher=data_fetcher,
        csv_handler=csv_handler,
    )
    city_coord.scrape()
    akiya_scrapper = AkiyaScraper(
        f"akiya_{CURRENT_DATE}.csv",
        PATH,
        login_handler,
        data_fetcher,
        csv_handler,
    )
    akiya_scrapper.scrape()



# This ensures the script is executed when run directly
if __name__ == "__main__":
    main()
