import logging
import time
import os


from akiya_scrapper.utils import dict_csv_list
from akiya_scrapper.config import akiya_config

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


# class AkiyaScraperV1:

#     def __init__(self, api: str, filename: str, path: str):
#         self.api = api
#         self.filename = filename
#         self.path = path
#         self.session = Session()
#         self.login_url = "https://www.akiya-mart.com/auth/login"
#         self.email = None
#         self.password = None
#         # self.login()

#     def login(self):
#         headers = {
#             "accept": "*/*",
#             "accept-language": "en-US,en;q=0.9,es-US;q=0.8,es;q=0.7",
#             "content-type": "application/json",
#             "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
#             "sec-ch-ua-mobile": "?0",
#             "sec-ch-ua-platform": '"macOS"',
#             "sec-fetch-dest": "empty",
#             "sec-fetch-mode": "cors",
#             "sec-fetch-site": "same-origin",
#         }
#         data = {"email": self.email, "password": self.password, "rememberMe": True}

#         response = self.session.post(self.login_url, headers=headers, json=data)
#         if response.status_code == 200:
#             logger.info("Login successful")
#         else:
#             logger.error(f"Login failed with status code {response.status_code}")
#             logger.error(response.text)
#             raise Exception("Authentication failed")

#     def flatten_dict(self, d, parent_key="", sep="_", index_offset=1):
#         """
#         Flatten a nested dictionary and generate flattened keys.

#         Parameters:
#         - d (dict): The dictionary to flatten.
#         - parent_key (str): The parent key for recursion.
#         - sep (str): The separator to use between parent and child keys.
#         - index_offset (int): The starting index for list elements.

#         Returns:
#         - dict: A flattened dictionary.
#         """
#         items = []
#         for k, v in d.items():
#             new_key = f"{parent_key}{sep}{k}" if parent_key else k
#             if isinstance(v, dict):
#                 items.extend(
#                     self.flatten_dict(
#                         v, new_key, sep=sep, index_offset=index_offset
#                     ).items()
#                 )
#             elif isinstance(v, list):
#                 if all(isinstance(i, str) for i in v):
#                     # If the list contains all strings, join them with a comma
#                     items.append((new_key, ",".join(v)))
#                 else:
#                     for i, item in enumerate(v, start=index_offset):
#                         items.extend(
#                             self.flatten_dict(
#                                 {f"{k}_{i}": item},
#                                 new_key,
#                                 sep=sep,
#                                 index_offset=index_offset,
#                             ).items()
#                         )
#             else:
#                 items.append((new_key, v))
#         return dict(items)

#     def get_data(self, url):
#         """
#         Fetch data from the URL using Pyppeteer to handle JavaScript rendering.

#         Parameters:
#         - url (str): The URL to fetch data from.

#         Returns:
#         - str: The HTML content of the page.
#         """
#         headers = {
#             "accept": "*/*",
#             "accept-language": "en-US,en;q=0.9,es-US;q=0.8,es;q=0.7",
#             "content-type": "application/json",
#             "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
#             "sec-ch-ua-mobile": "?0",
#             "sec-ch-ua-platform": '"macOS"',
#             "sec-fetch-dest": "empty",
#             "sec-fetch-mode": "cors",
#             "sec-fetch-site": "same-origin",
#             "Referer": "https://www.akiya-mart.com/explore",
#             "Referrer-Policy": "strict-origin-when-cross-origin",
#         }
#         try:
#             response = self.session.get(url, headers=headers)
#             response.raise_for_status()
#             return response.json()  # Assuming the response content is JSON
#         except HTTPError as http_err:
#             # Handle HTTP errors (e.g., 404 Not Found, 500 Internal Server Error)
#             logger.error(f"HTTP error occurred: {http_err}")
#             raise  # Re-raise the exception after handling
#         except Exception as err:
#             # Handle other types of exceptions
#             logger.error(f"An error occurred: {err}")
#             raise  # Re-raise the exception after handling

#     def dict_csv_list(self, data, attributes=akiya_config.listing_attributes):
#         """
#         Convert a dictionary to a CSV list based on ANIME_ATTRIBUTES.

#         Parameters:
#         - data (dict): The dictionary containing anime data.

#         Returns:
#         - list: A list representing the CSV row.
#         """

#         flattened_dict = self.flatten_dict(data)
#         csv_row = [flattened_dict.get(key, None) for key in attributes]
#         return csv_row

#     def scrape(self):
#         """
#         Fetch anime data from the API, convert it to a CSV list, and save it to a CSV file.
#         """
#         parent_dir = os.path.join(self.path, "csv_files")
#         os.makedirs(parent_dir, exist_ok=True)
#         csv_filepath = os.path.join(parent_dir, self.filename)
#         page = 1
#         last_page = akiya_config.last_page
#         chunk_size = akiya_config.chunk_size
#         csv_list = [akiya_config.listing_attributes]

#         with open(csv_filepath, "w", newline="", encoding="utf-8") as csvfile:
#             csv_writer = csv.writer(csvfile, delimiter="|")
#             csv_writer.writerow(akiya_config.listing_attributes)  # Write the header row

#             while page < last_page:
#                 base_url = self.api.format(page)
#                 result = self.get_data(base_url)
#                 listing = result.get("results", None)
#                 if not listing:
#                     logger.warning(f"No results found for page {page}")
#                     page += 1
#                     time.sleep(2)
#                     continue

#                 logger.info(f"Got results for page {page} out of {last_page}")
#                 csv_list.append(self.dict_csv_list(listing))

#                 if len(csv_list) >= chunk_size:
#                     csv_writer.writerows(csv_list[1:])
#                     csv_list = [
#                         akiya_config.listing_attributes
#                     ]  # Reset the list with header

#                 time.sleep(2)
#                 page += 1

#             # Write any remaining rows after the loop
#             if len(csv_list) > 1:
#                 csv_writer.writerows(csv_list[1:])


#         logger.info(f"CSV file '{self.filename}' created successfully.")
#         upload_to_s3(csv_filepath, akiya_config.bucket, self.filename)
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
