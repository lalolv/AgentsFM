from pymongo import MongoClient
from langchain_core.utils import get_from_env
from dotenv import load_dotenv
import random
import json
import pprint


load_dotenv()

# mongo
client = MongoClient(get_from_env("MONGODB_URL", "MONGODB_URL"))
db = client["agents_fm"]
col_playlist = db["playlist"]

# 读取音乐列表
with open('./data/tracks.json', 'r', encoding='utf8') as fp:
    # 解析json格式
    tracks = json.load(fp)
    # 随机排序
    random.shuffle(tracks)
    # 保存到数据集
    result = col_playlist.insert_many(tracks)
    print("Add count: {}".format(len(result.inserted_ids)))
