from datetime import datetime, timezone
from akiya_scrapper.akiya import AkiyaScraper
from akiya_scrapper.coord import CityCoord
from akiya_scrapper.utils import LoginHandler, DataFetcher, CSVHandler
from akiya_scrapper.config import akiya_config, JAPAN_CITIES, SHARED_VOLUME_PATH

# Get the current date and time for the filename
CURRENT_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")


def main(city: str):
    login_handler = LoginHandler(
        email=akiya_config.email, password=akiya_config.password
    )
    data_fetcher = DataFetcher(login_handler.get_session())
    csv_handler = CSVHandler()

    city_coord = CityCoord(
        login_handler=login_handler,
        data_fetcher=data_fetcher,
        city=city
    )
    city = city_coord.scrape()

    akiya_scrapper = AkiyaScraper(
        f"{CURRENT_DATE}_{city.city.lower()}.csv",
        SHARED_VOLUME_PATH,
        city,
        login_handler,
        data_fetcher,
        csv_handler,
    )
    akiya_scrapper.scrape()



# This ensures the script is executed when run directly
if __name__ == "__main__":
    for japan_city in JAPAN_CITIES:
        main(japan_city.name)
