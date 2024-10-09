import os
import pymongo
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB")
mongo_collection = os.getenv("MONGO_COLLECTION")

client = pymongo.MongoClient(mongo_uri)
db = client[mongo_db]
collection = db[mongo_collection]

# Azure Service Bus connection
servicebus_connection_string = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
servicebus_queue_name = os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME")

servicebus_client = ServiceBusClient.from_connection_string(servicebus_connection_string)
queue_name = servicebus_queue_name

# Function to send data to Azure Service Bus
def send_to_service_bus(data):
    with servicebus_client.get_queue_sender(queue_name) as sender:
        message = ServiceBusMessage(str(data))
        sender.send_messages(message)
        print(f"Sent message: {data}")

# Function to monitor MongoDB change stream
def monitor_change_stream():
    pipeline = [
        {"$match": {"operationType": {"$in": ["insert", "update", "replace"]}}},
        {"$project": {"_id": 1, "fullDocument": 1, "ns": 1, "documentKey": 1}}

    ]
    with collection.watch(pipeline, full_document='updateLookup') as stream:
        for change in stream:
            print(f"Detected change: {change}")
            send_to_service_bus(change)

# Start monitoring the change stream
if __name__ == "__main__":
    monitor_change_stream()