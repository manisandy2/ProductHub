from authtoken_01 import auth_token, nosql_database_connection
import datetime
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time

date = datetime.datetime.now().strftime("%d-%m-%Y")

load_dotenv()
file_name = "Product Data 1"

# Create directory for saving data
os.makedirs(date, exist_ok=True)


class Product:
    def __init__(self):
        self.link = f"{os.getenv('Baseurl')}{os.getenv('href')}"
        self.headers = {
            "Authorization": f"Bearer {auth_token()['auth']['access_token']}",
            "Accept": "application/json",
        }
        self.path = os.path.join(os.getcwd(), date, f"{file_name} {date}.xlsx")
        self.chunk_size = 10  # Number of pages to fetch concurrently

    def fetch_page(self, page):
        """Fetch a single page of data from the API."""
        try:
            response = requests.get(url=f"{self.link}{page}", headers=self.headers)
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            return []

    def product_loop(self):
        """Fetch all product data in chunks and save to Excel incrementally."""
        page = 1
        with ThreadPoolExecutor(max_workers=5) as executor:
            while True:
                # Fetch multiple pages concurrently
                pages = range(page, page + self.chunk_size)
                results = executor.map(self.fetch_page, pages)

                # Flatten the results and break if no more data
                items = [item for result in results for item in result]
                if not items:
                    break

                # Save to Excel incrementally
                self.save_to_excel(items, append=True)
                page += self.chunk_size

    def save_to_excel(self, data, append=False):
        """Save data to Excel incrementally."""
        df = pd.DataFrame(data)
        if not df.empty:
            with pd.ExcelWriter(self.path, mode='a' if append else 'w', engine='openpyxl') as writer:
                df.to_excel(writer, index=False, header=not append)


# Execution
start_time = time.time()

ss = Product()
ss.product_loop()

end_time = time.time()
elapsed_time = end_time - start_time

# Report execution time
if elapsed_time > 60:
    minutes, seconds = divmod(elapsed_time, 60)
    print(f"Total execution time: {int(minutes)} minutes and {seconds:.2f} seconds")
else:
    print(f"Total execution time: {elapsed_time:.2f} seconds")