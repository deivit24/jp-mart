import sys
import os
from datetime import datetime
from akiya_scrapper.akiya import AkiyaScraperV1


CURRENT_DATE = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
akiya = {
    "api": "https://www.akiya-mart.com/listings/id/{}?currency=usd",
    "filename": f"akiya_{CURRENT_DATE}.csv",
    "path": os.path.dirname(os.path.realpath(__file__)),
}


def main():
    scrape = AkiyaScraperV1(akiya["api"], akiya["filename"], akiya["path"])
    scrape.scrape()
    sys.exit()


if __name__ == "__main__":
    main()
