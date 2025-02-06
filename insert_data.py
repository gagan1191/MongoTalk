import time
import random
import string
import datetime
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017/"
client = None

# Retry mechanism to wait for MongoDB to be available
for attempt in range(5):
    try:
        client = MongoClient(MONGO_URI)
        db = client["test_db"]
        print("✅ Connected to MongoDB successfully.")
        break
    except Exception as e:
        print(f"⚠️ Attempt {attempt + 1}/5: MongoDB not ready, retrying...")
        time.sleep(3)

if client is None:
    print("❌ MongoDB connection failed after multiple attempts.")
    exit(1)


# Helper Functions to Generate Random Data
def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_email():
    return f"{random_string()}@example.com"

def random_status(choices=["active", "inactive", "pending"]):
    return random.choice(choices)

def random_date(start_year=2020, end_year=2023):
    start_date = datetime.datetime(start_year, 1, 1)
    end_date = datetime.datetime(end_year, 12, 31)
    return start_date + datetime.timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

def random_amount(min_amount=10, max_amount=1000):
    return round(random.uniform(min_amount, max_amount), 2)

# Insert Random Data into MongoDB
def insert_random_data():
    users_collection = db["users"]
    orders_collection = db["orders"]

    # Clear old data
    users_collection.delete_many({})
    orders_collection.delete_many({})
    print("🗑️ Cleared old data.")

    # Insert random users
    users_data = []
    for _ in range(100):
        user = {
            "name": random_string(random.randint(5, 10)).capitalize(),
            "email": random_email(),
            "created_at": random_date().isoformat(),
            "status": random_status(),
        }
        users_data.append(user)
    users_collection.insert_many(users_data)
    print(f"✅ Inserted {len(users_data)} users into 'users' collection.")

    # Insert random orders
    orders_data = []
    user_ids = [user["_id"] for user in users_collection.find({}, {"_id": 1})]  # Get user IDs
    for _ in range(100):
        order = {
            "order_id": f"ORD-{random.randint(1000, 9999)}",
            "user_id": random.choice(user_ids),  # Reference a random user
            "total": random_amount(),
            "status": random_status(["completed", "pending", "canceled"]),
            "created_at": random_date().isoformat(),
        }
        orders_data.append(order)
    orders_collection.insert_many(orders_data)
    print(f"✅ Inserted {len(orders_data)} orders into 'orders' collection.")

# Run the script
if __name__ == "__main__":
    insert_random_data()
