import json
from pymongo import MongoClient
from datetime import datetime

class MongoDBDataCleaner:
    def __init__(self, config_path, collection_name):
        with open(config_path) as f:
            config = json.load(f)
        # Set up MongoDB connection
        self.client = MongoClient(config["db_uri"])
        self.db = self.client[config["db_name"]]
        self.collection = self.db[collection_name]

    def limit_age(self, max_age=99):
        self.collection.update_many(
            {"age": {"$gt": max_age}},
            {"$set": {"age": max_age}}
        )

    def cap_purchase_amount(self, max_amount=1000):
        self.collection.update_many(
            {"purchase_amount": {"$gt": max_amount}},
            {"$set": {"purchase_amount": max_amount}}
        )

    def set_signup_date_limit(self, cutoff_date="2023-12-31"):
        cutoff_date = datetime.strptime(cutoff_date, "%Y-%m-%d")
        self.collection.update_many(
            {"signup_date": {"$gt": cutoff_date}},
            {"$set": {"signup_date": cutoff_date}}
        )

    def fill_missing_location(self, default_value="Unknown"):
        self.collection.update_many(
            {"location": {"$exists": False}},
            {"$set": {"location": default_value}}
        )

    def fill_missing_category(self, default_value="unknown"):
        self.collection.update_many(
            {"category": {"$exists": False}},
            {"$set": {"category": default_value}}
        )

    def clean_data(self):
        self.limit_age()
        self.cap_purchase_amount()
        self.set_signup_date_limit()
        self.fill_missing_location()
        self.fill_missing_category()

if __name__ == "__main__":
    cleaner = MongoDBDataCleaner(
        config_path="config.json",
        collection_name="sample_data"
    )
    cleaner.clean_data()
    print("Data cleaning operations completed.")
