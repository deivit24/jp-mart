import os
from datetime import datetime
from akiya_scrapper.akiya import AkiyaScraperV1
from akiya_scrapper.config import akiya_config

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/start/<secret>")
def scrape_akiya(secret):
    try:
        if secret != akiya_config.secret:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Unauthorized: Secret key does not match",
                    }
                ),
                403,
            )

        # Get the current date and time for the filename
        CURRENT_DATE = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        akiya = {
            "api": "https://www.akiya-mart.com/listings/id/{}?currency=usd",
            "filename": f"akiya_{CURRENT_DATE}.csv",
            "path": os.path.dirname(os.path.realpath(__file__)),
        }

        # Initialize the scraper with the given configuration
        scrape = AkiyaScraperV1(akiya["api"], akiya["filename"], akiya["path"])
        # Start the scraping process
        scrape.scrape()
        return jsonify({"status": "success", "message": "Scraping completed"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
