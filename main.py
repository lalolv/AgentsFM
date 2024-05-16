from dotenv import load_dotenv
import os
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
    feed_lang = input("Feed language [zh en]: ")
    feed_skip = int(input("Feed Skip: "))
    urls = []
    # 读取资源列表
    with open('/Volumes/AgentsFM/ai-dj.json', 'r', encoding='utf8') as items:
        aidjs = json.load(items)
        aidj_info = aidjs[aidj]
        urls.extend(aidj_info["feed_{}".format(feed_lang)])
        
    # 读取 tracks 文件
    with open('./data/tracks.json', 'r', encoding='utf8') as fp:
        # mq
        mq_host = os.getenv('mq_addr')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=mq_host, heartbeat=0))
        channel = connection.channel()
        channel.queue_declare(queue='agents-fm-ai-dj')
        # 解析json格式
        tracks = json.load(fp)
        # 随机排序
        random.shuffle(tracks)
        track_idx:int = 0
        # 读取新闻 zh en
        read_idx:int = 0
        loader = RSSFeedLoader(urls=urls, nlp=False, language=feed_lang)
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
            resfile = open("./data/human_eval.txt", "w", encoding="utf-8")
            resfile.write(result)
            resfile.close()
            # 人类评估
            eval_continue = input(
                "需要评估[{0}]，是否继续？Y / ys / n / s(Stop) -> ".format(read_idx+1))
            if eval_continue == '' or "y" in eval_continue.lower():
                # 从文件中读取新的文案
                with open('./data/human_eval.txt', 'r', encoding='utf8') as human_eval:
                    new_result = human_eval.read()
                    # message
                    push_msg = {
                        "script": new_result,
                        "role": aidj,
                        "track": track
                    }
                    # publish
                    channel.basic_publish(exchange='',
                                            routing_key='agents-fm-ai-dj',
                                            body=json.dumps(push_msg))
                    read_idx += 1
                # 如果超出播放列表，则重置 0
                if track_idx == len(tracks)-1:
                    track_idx = 0
                else:
                    track_idx += 1
                # yes and stop
                if eval_continue.lower() == "ys":
                    break
            elif eval_continue.lower() == 'n':
                # 重新生成
                print('跳过：{0}'.format(track["title"]))
            else:
                print('Stop!')
                break
            # sleep
            time.sleep(1)
        # close
        connection.close()
