import logging
import os
import requests
import datetime
from dotenv import load_dotenv, dotenv_values
# from pymongo import MongoClient

load_dotenv()
# run auth single time only

date = datetime.datetime.now().strftime("%d-%m-%Y")


config_token = {
    **dotenv_values(".env.token")
}

config_header = {
    **dotenv_values(".env.header")
}

# print(config_header)
# print(config_token)
# print(os.getenv("BaseUrl"))

def auth_token():
    try:
        base_url = os.getenv("BaseUrl")
        auth_url = os.getenv("AuthUrl")

        if not base_url or not auth_url:
            raise ValueError("Baseurl and AuthURl Environment Variable is Missing")
        response = requests.post(base_url+auth_url, headers=config_header, data=config_token)
        response.raise_for_status()

        data = {"status": response.status_code,
                "auth": response.json()}

        logging.info(f"Auth token Fetched successfully:{data['auth']}")
        return data
    except requests.RequestException as e:
        logging.error(f"Failed to fetch auth token: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise


# print(auth_token())


# def nosql_database_connection(data=None, client=None):
#     try:
#         # Connect to MongoDB (Replace this URL with your actual MongoDB connection URL)
#         client = MongoClient(os.getenv("Mongodb_Url") + os.getenv("MongoDB_Client"))
#         db = client[os.getenv("MongoDB_TableName")]
#         collection = db[date]  # Collection name based on current date

#         # Insert data into MongoDB collection
#         if data:
#             collection.insert_one(data)
#             logging.info("Data inserted successfully into MongoDB")
#         else:
#             logging.warning("No data provided for MongoDB insertion")
#     except Exception as e:
#         logging.error(f"Failed to insert data into MongoDB: {e}")
#         raise
#     finally:
#         client.close()  # Close the MongoDB connection after operation
#         logging.info("MongoDB connection closed")

# connectDBMongo()
