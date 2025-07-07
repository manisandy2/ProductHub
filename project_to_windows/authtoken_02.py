import os
import requests
import datetime
from dotenv import load_dotenv, dotenv_values
from pymongo import MongoClient
import logging

# Load environment variables
load_dotenv()

# Get current date for collection naming
date = datetime.datetime.now().strftime("%d-%m-%Y")

# Load tokens and headers from .env files
config_token = {**dotenv_values(".env.token")}
config_header = {**dotenv_values(".env.header")}

# Setup logging
logging.basicConfig(level=logging.INFO)


def auth_token():
    """Fetch authentication token from the API."""
    try:
        base_url = os.getenv("BaseUrl")
        auth_url = os.getenv("AuthUrl")
        if not base_url or not auth_url:
            raise ValueError("BaseUrl or AuthUrl environment variable is missing")

        # Make POST request to get auth token
        response = requests.post(base_url+auth_url, headers=config_header, data=config_token)

        # Check for successful response
        response.raise_for_status()

        data = {
            "status_code": response.status_code,
            "auth": response.json()
        }

        logging.info(f"Auth token fetched successfully: {data['auth']}")
        return data
    except requests.RequestException as e:
        logging.error(f"Failed to fetch auth token: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise


def connectDBMongo(data=None):
    """Connect to MongoDB and insert data."""
    try:
        print(os.getenv("Mongodb_Url"))
        print(os.getenv("MongoDB_Client"))
        # Connect to MongoDB (Replace this URL with your actual MongoDB connection URL)
        client = MongoClient(os.getenv("Mongodb_Url")+os.getenv("MongoDB_Client"))
        db = client[os.getenv("MongoDB_TableName")]
        collection = db[date]  # Collection name based on current date

        # Insert data into MongoDB collection
        if data:
            collection.insert_one(data)
            logging.info("Data inserted successfully into MongoDB")
        else:
            logging.warning("No data provided for MongoDB insertion")
    except Exception as e:
        logging.error(f"Failed to insert data into MongoDB: {e}")
        raise
    finally:
        client.close()  # Close the MongoDB connection after operation
        logging.info("MongoDB connection closed")

# Example usage


if __name__ == "__main__":
    # Fetch token
    try:
        token_data = auth_token()
        access_token = token_data["auth"]["access_token"]

        # Insert example data into MongoDB
        example_data = {
            "access_token": access_token,
            "fetched_at": datetime.datetime.now().isoformat()
        }
        connectDBMongo(example_data)
    except Exception as e:
        logging.error(f"Script failed: {e}")