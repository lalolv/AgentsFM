from dotenv import load_dotenv
import os, uuid
import json
import time, datetime
import pika
import random
from utils.strings import remove_newlines
from crews import FMCrew
from langchain_community.document_loaders import RSSFeedLoader
from agents import FMAgents
from tasks import FMTasks
from crewai import Crew, Process
from pymongo import MongoClient


# This is the main class that you will use to define your custom crew.
# You can define as many agents and tasks as you want in agents.py and tasks.py

load_dotenv()


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to AI Agents FM")
    print("-------------------------------")

    aidj = input("AI DJ [nancy ting xiao tong bai qiang john]: ")
    feed_tag = input("Feed Tag [zh en]: ")
    feed_skip = int(input("Feed Skip: "))
    feed_limit = int(input("Feed Limit: "))
    feed_idx:int = 0
    urls = []
    # 读取资源列表
    with open('/Volumes/AgentsFM/ai-dj.json', 'r', encoding='utf8') as items:
        aidjs = json.load(items)
        aidj_info = aidjs[aidj]
        urls.extend(aidj_info["feed_{}".format(feed_tag)])
        
    # 读取 tracks 文件
    with open('./data/tracks.json', 'r', encoding='utf8') as fp:
        # mq
        mq_host = os.getenv('mq_addr')
        # 解析json格式
        tracks = json.load(fp)
        # 随机排序
        random.shuffle(tracks)
        track_idx:int = 0
        # 读取新闻 zh en
        read_idx:int = 0
        loader = RSSFeedLoader(urls=urls, nlp=False, language=feed_tag)
        news_list = loader.load()
        # agent
        agents = FMAgents()
        tasks = FMTasks()
        # mongo
        client = MongoClient("mongodb://root:1128@192.168.50.177:27017")
        db = client["agents_fm"]
        col_aidj = db["ai_dj"]
        # 遍历新闻数据
        for news_item in news_list[feed_skip:]:
            # 音乐信息
            track = tracks[track_idx]
            # 新闻标题和内容
            title = news_item.metadata['title']
            link = news_item.metadata['link']
            content = news_item.page_content
            # Agent：writer
            writer = agents.scripts_content_writer()
            # 任务：撰写脚本
            draft_scripts = tasks.draft_news_scripts(
                writer, title, link, content)
            # Define crew
            crew = Crew(
                agents=[writer],
                tasks=[draft_scripts],
                verbose=True,
                process=Process.sequential
            )
            result = crew.kickoff()
            # 保存的数据
            msg = {
                "title": "xxx",
                "script": result,
                "role": aidj,
                "track": track,
                "date": datetime.datetime.now(),
                "status": 0
            }
            # resfile = open(
            #     "./human/{0}_{1}.json".format(aidj, crew.id.hex),
            #     "w", encoding="utf-8")
            # resfile.write(json.dumps(msg))
            # resfile.close()
            # 保存到 MongoDB
            script_id = col_aidj.insert_one(msg).inserted_id
            print("Script ID: {}".format(script_id))
            # 如果超出播放列表，则重置 0
            if track_idx == len(tracks)-1:
                track_idx = 0
            else:
                track_idx += 1
            # 计数器
            feed_idx += 1
            if feed_limit < feed_idx:
                break
            # Sleep
            time.sleep(6)
        # close
        client.close()