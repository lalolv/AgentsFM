from dotenv import load_dotenv
import os, uuid
import json
import time
import pika
import random
from utils.strings import remove_newlines
from crews import FMCrew
from langchain_community.document_loaders import RSSFeedLoader


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
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=mq_host, heartbeat=0))
        channel = connection.channel()
        channel.queue_declare(queue='agents-fm-ai-human')
        # 解析json格式
        tracks = json.load(fp)
        # 随机排序
        random.shuffle(tracks)
        track_idx:int = 0
        # 读取新闻 zh en
        read_idx:int = 0
        loader = RSSFeedLoader(urls=urls, nlp=False, language=feed_tag)
        news_list = loader.load()
        # 遍历新闻数据
        fm_crew = FMCrew()
        for news_item in news_list[feed_skip:]:
            # 音乐信息
            track = tracks[track_idx]
            # 新闻标题和内容
            title = news_item.metadata['title']
            link = news_item.metadata['link']
            content = news_item.page_content
            result = fm_crew.broadcasting_news(title, content, link)
            # 写入文件
            msg = {
                "script": result,
                "role": aidj,
                "track": track
            }
            file_name = uuid.uuid4()
            resfile = open(
                "./human/{0}_{1}.json".format(aidj, file_name.hex), 
                "w", encoding="utf-8")
            resfile.write(json.dumps(msg))
            resfile.close()
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
        connection.close()
