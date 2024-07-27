import logging
from argparse import ArgumentParser

from akiya_scrapper.utils import CSVHandler

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def main(path: str):

    csv_handler = CSVHandler()
    data = csv_handler.read_csv_to_list(path)
    logger.info(f"Total Current Listings: {len(data)}")
    listing_ids = [int(d["listing_id"]) for d in data]
    logger.info(f"Total Listing IDS: {len(listing_ids)}")
    unique_listing_ids = list(set(listing_ids))
    logger.info(f"Total Unique Listing IDs: {len(unique_listing_ids)}")


if __name__ == "__main__":
    parser = ArgumentParser(description="Process a CSV file and count unique listings.")
    parser.add_argument("path", type=str, help="Path to the CSV file")
    args = parser.parse_args()

    main(args.path)
