from authtoken_01 import auth_token, nosql_database_connection
import datetime
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import time

# code was run but little slow
date = datetime.datetime.now().strftime("%d-%m-%Y")

load_dotenv()
file_name = "Product Data "

try:
    os.mkdir(date)
except OSError as e:
    print(e)


class Product:
    def __init__(self):
        self.master = []
        self.data = list[str]
        self.link = str(os.getenv("Baseurl")) + str(os.getenv("href"))
        self.i: int = 1101
        self.pd = pd
        self.path = os.getcwd()+"\\" + date + "\\" + file_name + "03" + " " + date + ".xlsx"
        self.folder = os.getcwd()+"\\" + date + "\\"
        self.status = auth_token()["status"]
        self.save_to_range = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]
        self.headers = {
                        "Authorization": "Bearer {}".format(auth_token()["auth"]["access_token"]),
                        "Accept": "application/json"
                    }

    def product_get(self):
        # try:
        self.data = requests.get(url=self.link+str(self.i), headers=self.headers)
        print(self.data.status_code)
        if self.data.status_code == 401:
            print("*"*200)
            print("Create Auth new call")
            auth_token()
            print(self.headers)
            self.headers.clear()
            print(self.headers)

            self.headers = {
                "Authorization": "Bearer {}".format(auth_token()["auth"]["access_token"]),
                "Accept": "application/json"
            }

            print(self.headers)
            print("Now create new auth")
            self.data = requests.get(url=self.link + str(self.i), headers=self.headers)
            print(self.data)
            print(self.data.status_code)
            print("*"*200)

            # print(self.data.text)
            # print("items", self.data.text)
            # print("items", type(self.data.text))
            # print("items 0", self.data.text)
            # print("items 0 0", self.data.content[2])
            # print("new len", len(self.data.json()["items"]))
            # print("new items", self.data.json()["items"])
            # for da in self.data.json()["items"]:
            #     # print(da)
            #     print(da["id"],da["name"],da["description"],da["brand_id"],
            #           da["brand_name"],da["category_id"],da["category_name"],
            #           da["sku_code"],da["min_price"],da["max_price"],da["indicative_price"]
            #
            #           )
            # print("links", self.data.json()["links"])
            # self.data.raise_for_status()
            # self.headers
        # except requests.exceptions.RequestException as e:
        #     print(f"Error fetching data: {e}")
        #     print("Last Range :", self.i)
        #     print("Status :", self.status)
        #     print("Data status",self.data.status_code)
        #     self.save_to_excel()
        #     print("*"*100)
        #
        #     print("*"*100)
            # exit()
        return self.data

    def print_range(self):
        print("Range :", self.i)

    def range_add(self):
        self.i = self.i + 1
        if self.i in self.save_to_range:
            self.save_to_excel()
            print(self.i, "value to save Range")
        if self.i == 1200:
            self.save_to_excel()
            exit()

    def json_length(self):
        print("Length :", len(self.master))

    def save_to_excel(self):
        self.pd.DataFrame(data=self.master).to_excel(self.path, index=False)

    def product_loop(self):
        while self.i:
            # print(auth_token()["auth"]["access_token"])
            self.print_range()
            self.product_get()
            self.product_data()
            self.range_add()
            self.json_length()
            # self.create_text()

    def product_data(self):
        # self.master.extend(self.data.json().get('items', []))
        self.master += self.data.json()['items']
        # print(self.data.json())
        # nosql_database_connection(data=self.data.json())

    # def create_text(self):
    #     text = open(self.folder+"range.txt", "w")
    #     text.write("{}".format(int(self.i)))
    #     text.close()
        # print(text)


start_time = time.time()
ss = Product()
# ss.create_text()
ss.product_loop()


end_time = time.time()
elapsed_time = end_time - start_time
print(f"Total execution time: {elapsed_time:.2f} seconds")

if elapsed_time > 60:
    minutes, seconds = divmod(elapsed_time, 60)
    print(f"Total execution time: {int(minutes)} minutes and {seconds:.2f} seconds")
