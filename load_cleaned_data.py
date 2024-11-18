from pymongo import MongoClient
import pandas as pd

def fetch_data():
    client = MongoClient("mongodb://localhost:27017")
    db = client["thesis_project"]
    collection = db["sample_data"]
    data = pd.DataFrame(list(collection.find()))
    data.drop(columns=['_id'], inplace=True)
    return data

if __name__ == "__main__":
    data = fetch_data()
    print(data.head())
