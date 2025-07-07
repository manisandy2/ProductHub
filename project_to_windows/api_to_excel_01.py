from authtoken_01 import auth_token,nosql_database_connection
import datetime
import requests
import os
from dotenv import load_dotenv
import pandas as pd


date = datetime.datetime.now().strftime("%d-%m-%Y")

load_dotenv()
file_name = "Product Data"

try:
    os.mkdir(date)
except OSError as e:
    print(e)


class Product:
    def __init__(self, date):
        self.date = date
        self.master = []
        self.data = list[str]
        self.base_url = os.getenv("Baseurl")
        self.href = os.getenv("href")
        self.i: int = 1
        self.file_path = os.path.join(os.getcwd(), date, f"{date}{file_name}.xlsx")
        # self.file_path = os.getcwd()+"\\" + date + "\\" + file_name + " " + date + ".xlsx"
        self.headers = {
            "Authorization": "Bearer {}".format(auth_token()["auth"]["access_token"]),
            "Accept": "application/json"
        }
        self.pd = pd

    def get_product(self):
        link = f"{self.base_url}{self.href}{self.i}"
        # self.data = requests.get(url=self.link+str(self.i), headers=self.headers)
        response = requests.get(link, headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to retrieve data at page {self.i} . last page:{self.i}")
            self.save_to_excel()
        self.master += response.json()['items']

    def print_range(self):
        print(f"Processing page {self.i}")

    def json_length(self):
        print("Length :", len(self.master))

    def increment_range(self):
        self.i += 1
        if self.i == 900:
            self.save_to_excel()
            exit()
        if (self.i-1) * 100 != len(self.master):
            print('range', (self.i-1))
            print("test", (self.i-1) * 100)
            print("master", len(self.master))
            self.save_to_excel()
            exit()

    def save_to_excel(self):
        self.pd.DataFrame(data=self.master).to_excel(self.file_path, index=False)

    def product_loop(self):
        self.i = 1
        while self.i:
            self.print_range()
            self.get_product()
            self.increment_range()
            self.json_length()

    def product_data(self):
        nosql_database_connection(data=self.master)


ss = Product(date)
ss.product_loop()
ss.product_data()

# 1 to 369
# 369 to 649
# 679 to 720
