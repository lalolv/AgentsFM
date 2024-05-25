import streamlit as st
import os
import json
import pika
from pymongo import MongoClient
import datetime


queue_host = '192.168.50.177'
push_topic = 'agents-fm-ai-dj'

# mongo
client = MongoClient("mongodb://root:1128@192.168.50.177:27017")
db = client["agents_fm"]
col_aidj = db["ai_dj"]
# col_aidj.create_index([("timer", 1)], expireAfterSeconds=360)

st.header('AI Agents FM :blue[Human!] :sunglasses:', divider='rainbow')

# 获取数据
filter = {"status": 0}
item = col_aidj.find_one(filter)
count = col_aidj.count_documents(filter)

# 更新数据状态
def update_status():
    col_aidj.update_one(
        {"_id": item["_id"]},
        {
            "$set": {
                "status": 1,
                "timer": datetime.datetime.now(datetime.UTC)
            }
        }
    )
    client.close()
    st.rerun()

if item is None:
    st.warning('没有发现文件', icon="⚠️")
else:
    # print(message)
    # 统计
    st.subheader("_待处理数量_ :blue[{}]".format(count))
    # title
    txt_title = st.text_input(label="标题", value=item["title"])
    # content
    txt_content = st.text_area(
        label="评审内容",
        value=item['script'],
        placeholder="加载内容...",
        height=600
    )
    # role
    st.text(item['role'])
    # track
    st.write(item["track"])

    # push button
    if st.button(label="推送", type="primary"):
        push_msg = {
            "title": txt_title,
            "script": txt_content,
            "role": item['role'],
            "track": item['track']
        }
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=queue_host))
        channel = connection.channel()
        channel.queue_declare(queue=push_topic)
        channel.basic_publish(exchange='',
                            routing_key=push_topic,
                            body=json.dumps(push_msg))
        connection.close()
        # update
        update_status()

    # push button
    if st.button(label="跳过"):
        # update
        update_status()
