import logging
import csv
import os
from requests import Session
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


class LoginHandler:
    def __init__(self, email, password):
        self.session = Session()
        self.login_url = "https://www.akiya-mart.com/auth/login"
        self.email = email
        self.password = password

    def login(self):
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,es-US;q=0.8,es;q=0.7",
            "content-type": "application/json",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }
        data = {"email": self.email, "password": self.password, "rememberMe": True}

        response = self.session.post(self.login_url, headers=headers, json=data)
        if response.status_code == 200:
            logger.info("Login successful")
        else:
            logger.error(f"Login failed with status code {response.status_code}")
            logger.error(response.text)
            raise Exception("Authentication failed")

    def get_session(self):
        return self.session


class DataFetcher:
    def __init__(self, session):
        self.session = session

    def get_data(self, url):
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,es-US;q=0.8,es;q=0.7",
            "content-type": "application/json",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "Referer": "https://www.akiya-mart.com/explore",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            raise
        except Exception as err:
            logger.error(f"An error occurred: {err}")
            raise


class CSVHandler:
    @staticmethod
    def write_to_csv(csv_list, csv_filepath):
        with open(csv_filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(csv_list)
        logger.info(f"CSV file '{csv_filepath}' created successfully.")

    @staticmethod
    def read_csv_to_list(csv_filepath: str):
        if not os.path.exists(csv_filepath):
            logger.error(f"CSV file '{csv_filepath}' does not exist.")
            return []

        with open(csv_filepath, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data

    @staticmethod
    def remove_duplicates(data: list, key):
        unique_data_dict = {}
        for item in data:
            item_key = item.get(key)
            if item_key and item_key not in unique_data_dict:
                unique_data_dict[item_key] = item
        return list(unique_data_dict.values())

    @staticmethod
    def append_to_csv(csv_list, csv_filepath):
        if not os.path.exists(csv_filepath):
            logger.error(f"CSV file '{csv_filepath}' does not exist.")
            return

        with open(csv_filepath, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(csv_list)


def flatten_dict(d, parent_key="", sep="_", index_offset=1):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(
                flatten_dict(v, new_key, sep=sep, index_offset=index_offset).items()
            )
        elif isinstance(v, list):
            if all(isinstance(i, str) for i in v):
                items.append((new_key, ",".join(v)))
            else:
                for i, item in enumerate(v, start=index_offset):
                    items.extend(
                        flatten_dict(
                            {f"{k}_{i}": item},
                            new_key,
                            sep=sep,
                            index_offset=index_offset,
                        ).items()
                    )
        else:
            items.append((new_key, v))
    return dict(items)


def dict_csv_list(data, attributes):
    flattened_dict = flatten_dict(data)
    csv_row = [flattened_dict.get(key, None) for key in attributes]
    return csv_row


def divide_rectangle(ne_lon, ne_lat, sw_lon, sw_lat, num_sections=10):
    # Determine the number of sections along each axis
    num_sections_per_axis = int(num_sections**0.5)  # Assuming a square grid of sections

    # Calculate the size of each section
    lon_interval = (ne_lon - sw_lon) / num_sections_per_axis
    lat_interval = (ne_lat - sw_lat) / num_sections_per_axis

    # List to hold the smaller rectangles
    rectangles = []

    # Generate the smaller rectangles
    for i in range(num_sections_per_axis):
        for j in range(num_sections_per_axis):
            # Define the southwest and northeast corners for each rectangle
            rect_sw_lon = sw_lon + i * lon_interval
            rect_sw_lat = sw_lat + j * lat_interval
            rect_ne_lon = rect_sw_lon + lon_interval
            rect_ne_lat = rect_sw_lat + lat_interval

            rectangles.append(
                {
                    "sw_lon": rect_sw_lon,
                    "sw_lat": rect_sw_lat,
                    "ne_lon": rect_ne_lon,
                    "ne_lat": rect_ne_lat,
                }
            )

    return rectangles
