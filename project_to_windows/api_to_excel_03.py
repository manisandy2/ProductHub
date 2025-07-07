import datetime
import requests
import os
import time
import logging
import pandas as pd
from dotenv import load_dotenv
from authtoken_01 import auth_token

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# Date-based directory setup
date = datetime.datetime.now().strftime("%d-%m-%Y")
file_name = "Product Data 1"
output_dir = os.path.join(os.getcwd(), date)
os.makedirs(output_dir, exist_ok=True)

# File path
file_path = os.path.join(output_dir, f"{file_name} {date}.xlsx")


class Product:
    def __init__(self):
        self.session = requests.Session()
        self.master = []
        self.page = 1
        self.base_url = os.getenv("Baseurl") + os.getenv("href")
        self.token = self.refresh_token()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        })

    def refresh_token(self):
        """Fetch a new auth token and update headers."""
        token_data = auth_token()
        return token_data["auth"]["access_token"]

    def fetch_products(self):
        """Fetch product data from the API."""
        url = f"{self.base_url}{self.page}"
        response = self.session.get(url)

        if response.status_code == 401:
            logging.warning("Unauthorized request. Refreshing token...")
            self.token = self.refresh_token()
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            response = self.session.get(url)

        if response.status_code != 200:
            logging.error(f"Failed to fetch data: {response.status_code} - {response.text}")
            return []

        return response.json().get("items", [])

    def save_to_excel(self):
        """Save data to an Excel file in batches."""
        if self.master:
            df = pd.DataFrame(self.master)
            df.to_excel(file_path, index=False)
            logging.info(f"Saved {len(self.master)} records to Excel.")
            self.master.clear()

    def run(self):
        """Main loop to fetch and process product data."""
        start_time = time.time()

        while self.page:
            logging.info(f"Fetching page: {self.page}")
            products = self.fetch_products()

            if not products:
                logging.info("No more data to fetch. Stopping...")
                break

            self.master.extend(products)

            # Save to Excel every 500 records to optimize memory usage
            if len(self.master) >= 500:
                self.save_to_excel()

            self.page += 1

            # Stop at 1000 pages (for safety)
            if self.page == 1000:
                logging.info("Reached 1000 pages. Stopping...")
                break

        # Final save
        self.save_to_excel()

        elapsed_time = time.time() - start_time
        logging.info(f"Total execution time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    Product().run()