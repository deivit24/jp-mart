import csv
import glob
import os
import re

from psycopg2 import connect
from decouple import config
from datetime import datetime, timezone

from akiya_scrapper.config import SHARED_VOLUME_PATH

CURRENT_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

CSV_PATH = f"{SHARED_VOLUME_PATH}/"
CSV_PATTERN = "*.csv"

OUTPUT_FILE = f"{CSV_PATH}{CURRENT_DATE}_latest.csv"

def get_latest_csv(directory, pattern):
    # Create the full path pattern
    full_pattern = os.path.join(directory, pattern)

    # Get a list of files matching the pattern
    files = glob.glob(full_pattern)

    # Define regex pattern for expected filenames
    regex = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_.+\.csv$")

    # Filter out files that don't match the expected format
    valid_files = [f for f in files if regex.match(os.path.basename(f))]

    print(valid_files)
    # If no files found, return None
    if not valid_files:
        return None

    # Sort the files based on the datetime part of their names
    valid_files.sort(
        key=lambda x: datetime.strptime(
            os.path.basename(x).rsplit("_", 1)[0],  # Extract everything before the last '_'
            "%Y-%m-%d_%H-%M-%S"
        ),
        reverse=True,
    )


    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as fout:
        writer = None

        for i, file in enumerate(valid_files):
            with open(file, 'r', encoding='utf-8') as fin:
                reader = csv.reader(fin)
                headers = next(reader)

                if writer is None:
                    writer = csv.writer(fout)
                    writer.writerow(headers)  # Write header only once

                for row in reader:
                    writer.writerow(row)
    # Delete the original valid files after merging
    for file in valid_files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Failed to delete {file}: {e}")

    # Return the most recent file
    return os.path.basename(OUTPUT_FILE)



DB_PARAMS = {
    "host": config("POSTGRES_HOST"),
    "database": config("POSTGRES_DB"),
    "user": config("POSTGRES_USER"),
    "password": config("POSTGRES_PASSWORD"),
}



def generate_sql():
    # Get the most recent CSV file
    latest_jp_mart_file = get_latest_csv(CSV_PATH, CSV_PATTERN)
    sql_script = f"""
    DROP SCHEMA IF EXISTS akiya CASCADE;
    CREATE SCHEMA IF NOT EXISTS akiya;
    DROP TABLE IF EXISTS akiya.listings;
    
    CREATE TABLE akiya.listings (
        listing_id integer primary key,
        city text,
        akiya_type text,
        construction_year integer,
        gross_yield decimal,
        is_featured boolean,
        is_liked boolean,
        kind text,
        lat double precision,
        like_count integer,
        lon double precision,
        prefecture text,
        price_foreign decimal,
        price_yen integer,
        translated_address text,
        view_count integer,
        image_urls text
    
    );
    
    
    COPY akiya.listings (
        listing_id,
        city,
        akiya_type,
        construction_year,
        gross_yield,
        is_featured,
        is_liked,
        kind,
        lat,
        like_count,
        lon,
        prefecture,
        price_foreign,
        price_yen,
        translated_address,
        view_count,
        image_urls
    )
    FROM '{CSV_PATH}{latest_jp_mart_file}' CSV HEADER DELIMITER ',' QUOTE '"';
    """

    return sql_script

def ingestion():
    sql_script = generate_sql()
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
