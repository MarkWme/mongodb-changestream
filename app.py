import os
import pymongo
import schedule
import time
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB")
mongo_collection = os.getenv("MONGO_COLLECTION")

client = pymongo.MongoClient(mongo_uri)
db = client[mongo_db]
collection = db[mongo_collection]

# Function to generate random business data
def generate_random_data():
    phone_models = ["iPhone 13", "Samsung Galaxy S21", "Google Pixel 6", "OnePlus 9"]
    data = {
        "model": random.choice(phone_models),
        "price": round(random.uniform(300, 1200), 2),
        "stock_level": random.randint(1, 100)
    }
    return data

# Function to write data to MongoDB
def write_data_to_mongodb():
    data = generate_random_data()
    collection.insert_one(data)
    print(f"Inserted data: {data}")

# Schedule the task to run every second
schedule.every(1).second.do(write_data_to_mongodb)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)