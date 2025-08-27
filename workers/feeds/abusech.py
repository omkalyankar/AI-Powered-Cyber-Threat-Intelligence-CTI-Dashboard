import requests
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
client = MongoClient(MONGO_URI)
db = client[os.getenv("MONGO_DB", "cti")]

def run():
    url = "https://sslbl.abuse.ch/blacklist/sslipblacklist.csv"
    r = requests.get(url)
    lines = r.text.splitlines()
    for l in lines:
        if l.startswith("#"): 
            continue
        ip = l.strip()
        if ip:
            db.iocs.update_one(
                {"type": "ip", "value": ip},
                {"$set": {"source": "abuse.ch"}},
                upsert=True
            )
    print("[+] Abuse.ch IOCs updated")
