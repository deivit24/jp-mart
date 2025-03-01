import glob
import os
import subprocess

from psycopg2 import connect
from decouple import config
from datetime import datetime


DOCKER_CONTAINER_NAME = "jp-mart-db"
DOCKER_PATH = "/usr/local"

CSV_PATH = "csv_files/"
CSV_PATTERN = "akiya_*.csv"


def get_latest_csv(directory, pattern):
    # Create the full path pattern
    full_pattern = os.path.join(directory, pattern)
    # Get a list of files matching the pattern
    files = glob.glob(full_pattern)

    # If no files found, return None
    if not files:
        return None

    # Sort the files based on the datetime part of their names
    files.sort(
        key=lambda x: datetime.strptime(
            os.path.basename(x), "akiya_%Y-%m-%d_%H-%M-%S.csv"
        ),
        reverse=True,
    )

    # Return the most recent file
    return os.path.basename(files[0])


# Get the most recent CSV file
latest_jp_mart_file = get_latest_csv(CSV_PATH, CSV_PATTERN)


JP_MART_PATH = os.path.abspath(os.path.join(CSV_PATH, latest_jp_mart_file))


CSV_PATH_LIST = [JP_MART_PATH]

DB_PARAMS = {
    "host": config("POSTGRES_HOST"),
    "database": config("POSTGRES_DB"),
    "user": config("POSTGRES_USER"),
    "password": config("POSTGRES_PASSWORD"),
}


def copy_to_docker(from_path, container_name, to_path):
    try:
        subprocess.run(
            ["docker", "cp", from_path, f"{container_name}:{to_path}"],
            check=True,
            text=True,
        )
        print(
            f"File copied from {from_path} to {container_name}:{to_path} successfully."
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running the 'docker cp' command: {e}")
    except FileNotFoundError:
        print(
            "Docker command not found. Make sure Docker is installed and available in your PATH."
        )


for csv_path in CSV_PATH_LIST:
    copy_to_docker(csv_path, DOCKER_CONTAINER_NAME, DOCKER_PATH)


sql_script = f"""

DROP SCHEMA IF EXISTS akiya CASCADE;
CREATE SCHEMA IF NOT EXISTS akiya;
DROP TABLE IF EXISTS akiya.listings;

CREATE TABLE akiya.listings (
    address text,
    building_area decimal,
    construction_year integer,
    description text,
    first_seen_at timestamp,
    gross_yield decimal,
    has_free_parking boolean,
    image_urls text,
    is_condo boolean,
    is_geocoded boolean,
    is_hidden boolean,
    is_liked boolean,
    is_toushi boolean,
    land_area text,
    last_seen_at timestamp,
    lat double precision,
    like_count integer,
    listing_id integer PRIMARY KEY,
    llm_area text,
    llm_description text,
    lon double precision,
    management_fee_foreign decimal,
    management_fee_yen integer,
    needs_update boolean,
    prefecture text,
    price_foreign decimal,
    price_yen integer,
    remarks text,
    repair_fee_foreign decimal,
    repair_fee_yen integer,
    station_distance text,
    station_lat double precision,
    station_lon double precision,
    station_name text,
    translated_address text,
    translated_condition text,
    translated_description text,
    translated_remarks text,
    url text
);


COPY akiya.listings (
    address,
    building_area,
    construction_year,
    description,
    first_seen_at,
    gross_yield,
    has_free_parking,
    image_urls,
    is_condo,
    is_geocoded,
    is_hidden,
    is_liked,
    is_toushi,
    land_area,
    last_seen_at,
    lat,
    like_count,
    listing_id,
    llm_area,
    llm_description,
    lon,
    management_fee_foreign,
    management_fee_yen,
    needs_update,
    prefecture,
    price_foreign,
    price_yen,
    remarks,
    repair_fee_foreign,
    repair_fee_yen,
    station_distance,
    station_lat,
    station_lon,
    station_name,
    translated_address,
    translated_condition,
    translated_description,
    translated_remarks,
    url
)
FROM '/usr/local/{latest_jp_mart_file}' CSV HEADER DELIMITER '|' QUOTE '"';
"""

try:
    # Connect to the PostgreSQL database
    connection = connect(**DB_PARAMS)

    # Create a cursor object
    cursor = connection.cursor()

    # Execute the SQL script, passing the full paths as parameters
    cursor.execute(sql_script)

    # Commit the changes
    connection.commit()

    print("SQL script executed successfully.")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
