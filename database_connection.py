import json
import pandas as pd
from pymongo import MongoClient

# Load configuration from config.json
with open('config.json') as f:
    config = json.load(f)

# Set up MongoDB connection
client = MongoClient(config["db_uri"])
db = client[config["db_name"]]
collection = db["sample_data"]

# Load data from CSV file and insert into MongoDB
data = pd.read_csv("sample_customer_data.csv")
data_json = data.to_dict(orient="records")

collection.insert_many(data_json)
print("Data successfully loaded into MongoDB!")

# Convert signup_date field to Date format in MongoDB
collection.update_many(
    {},
    [{"$set": {"signup_date": {"$toDate": "$signup_date"}}}]
)
print("signup_date field successfully converted to Date format in MongoDB!")
