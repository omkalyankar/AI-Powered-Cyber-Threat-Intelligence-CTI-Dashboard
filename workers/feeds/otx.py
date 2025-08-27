import requests, os
from pymongo import MongoClient

OTX_KEY = os.getenv("OTX_API_KEY", "")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
client = MongoClient(MONGO_URI)
db = client[os.getenv("MONGO_DB", "cti")]

def run():
    if not OTX_KEY:
        print("[!] No OTX API key set, skipping OTX")
        return
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {"X-OTX-API-KEY": OTX_KEY}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("[!] OTX error", r.text)
        return
    pulses = r.json().get("results", [])
    for p in pulses:
        for ind in p.get("indicators", []):
            db.iocs.update_one(
                {"type": ind.get("type"), "value": ind.get("indicator")},
                {"$set": {"source": "OTX", "title": p.get("name")}},
                upsert=True
            )
    print("[+] OTX IOCs updated")
