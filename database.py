import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

client = pymongo.MongoClient(os.environ["MONGO_URL"])
db = client["mumble-link"]
links = db["links"]
hashes = db["hashes"]