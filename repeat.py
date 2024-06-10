from pymongo import MongoClient
from langchain_core.utils import get_from_env
from dotenv import load_dotenv
from utils.console import print_ok, print_header
import time
import json
import pika


load_dotenv()
push_topic = "agents-fm-live"

print_header("## Welcome to AI Agents FM")
print("-------------------------------")
repeat_limit = int(input("Repeat Limit: "))

# mongo
client = MongoClient(get_from_env("MongoDB URL", "MONGODB_URL"))
db = client["agents_fm"]
col_recently = db["recently_played"]

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=get_from_env("MQ Host", "MQ_HOST")))
channel = connection.channel()
channel.queue_declare(queue=push_topic, durable=True)

filter = {}
for item in col_recently.find(filter).limit(repeat_limit):
    push_msg = json.dumps({
        "title": item["title"],
        "subtitle": item["subtitle"],
        "avatar": item["avatar"],
        "cover": item["cover"],
        "file": item["file"]
    })
    channel.basic_publish(
        exchange='', routing_key=push_topic, body=push_msg,
        properties=pika.BasicProperties(delivery_mode=2))
    # remove data
    col_recently.delete_one({"_id": item["_id"]})
    # sleep
    time.sleep(2)

connection.close()
