import logging
import csv
import os
from requests import Session
from requests.exceptions import HTTPError
from tenacity import retry, stop_after_attempt, wait_fixed


def setup_logger(name, log_file=None, level=logging.INFO):
    """
    Function to set up a logger with both console and file handlers.

    :param name: Name of the logger.
    :param log_file: Path to the log file. If None, logs will not be saved to a file.
    :param level: Logging level (default: logging.INFO).
    :return: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    if log_file:
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        # Create a file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


error_logger = setup_logger(
    __file__, log_file="akiya_scrapper/logs/error.log", level=logging.ERROR
)


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
        data = {"emailOrUsername": self.email, "password": self.password, "rememberMe": True}

        response = self.session.post(self.login_url, headers=headers, json=data)
        if response.status_code == 200:
            error_logger.info("Login successful")
        else:
            error_logger.error(f"Login failed with status code {response.status_code}")
            error_logger.error(response.text)
            raise Exception("Authentication failed")

    def get_session(self):
        return self.session


class DataFetcher:
    def __init__(self, session):
        self.session = session

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(10))
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
            error_logger.error(f"HTTP error occurred: {http_err}")
            raise
        except Exception as err:
            error_logger.error(f"An error occurred: {err}")
            raise


class CSVHandler:
    @staticmethod
    def write_to_csv(csv_list, csv_filepath):
        with open(csv_filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(csv_list)
        error_logger.info(f"CSV file '{csv_filepath}' created successfully.")

    @staticmethod
    def read_csv_to_list(csv_filepath: str):
        if not os.path.exists(csv_filepath):
            error_logger.error(f"CSV file '{csv_filepath}' does not exist.")
            return []

        with open(csv_filepath, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data

    @staticmethod
    def remove_duplicates(data: list, key) -> list:
        unique_data_dict = {}
        for item in data:
            item_key = item.get(key)
            if item_key and item_key not in unique_data_dict:
                unique_data_dict[item_key] = item
        return list(unique_data_dict.values())

    @staticmethod
    def append_to_csv(csv_list, csv_filepath):
        if not os.path.exists(csv_filepath):
            error_logger.error(f"CSV file '{csv_filepath}' does not exist.")
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


def divide_rectangle(ne_lon, ne_lat, sw_lon, sw_lat, num_sections_per_axis=10):
    # Determine the horizontal and vertical distances
    horizontal_distance = ne_lon - sw_lon
    vertical_distance = ne_lat - sw_lat

    # Adjust to form a square
    if horizontal_distance > vertical_distance:
        # Adjust latitude to match longitude distance
        adjusted_ne_lat = sw_lat + horizontal_distance
        adjusted_ne_lon = ne_lon
    else:
        # Adjust longitude to match latitude distance
        adjusted_ne_lon = sw_lon + vertical_distance
        adjusted_ne_lat = ne_lat

    # Assuming a square grid of sections
    # Calculate the size of each section
    lon_interval = (adjusted_ne_lon - sw_lon) / num_sections_per_axis
    lat_interval = (adjusted_ne_lat - sw_lat) / num_sections_per_axis

    # List to hold the smaller squares
    squares = []

    # Generate the smaller rectangles
    for i in range(num_sections_per_axis):
        for j in range(num_sections_per_axis):
            # Define the southwest and northeast corners for each rectangle
            rect_sw_lon = sw_lon + i * lon_interval
            rect_sw_lat = sw_lat + j * lat_interval
            rect_ne_lon = rect_sw_lon + lon_interval
            rect_ne_lat = rect_sw_lat + lat_interval

            squares.append(
                {
                    "sw_lon": rect_sw_lon,
                    "sw_lat": rect_sw_lat,
                    "ne_lon": rect_ne_lon,
                    "ne_lat": rect_ne_lat,
                }
            )

    return squares


def count_mapping(count: int) -> int:
    """
    This function is going to take in a count of the total listings of the city
    and will return a number that will be divided by the coordinates of said city

    Args:
        count: (int)

    Return:
        int: This will be the total number
    """
    if count < 1000:
        return 4
    elif count < 3000:
        return 6
    elif count < 6000:
        return 10
    elif count < 8000:
        return 12
    elif count < 10000:
        return 14
    elif count < 12000:
        return 16
    else:
        return 18
