import streamlit as st
import os
import json
import pika


queue_host = '192.168.50.177'
push_topic = 'agents-fm-ai-dj'

st.header('AI Agents FM :blue[Human!] :sunglasses:', divider='rainbow')

file_name:str = ''
path = './human'
files = os.listdir(path)

if len(files) == 0:
    st.warning('没有发现文件', icon="⚠️")
else:
    with open(os.path.join(path, files[0]), 'r', encoding='utf8') as fp:
        message = json.load(fp)
        # print(message)
        # text
        txt = st.text_area(
            label="评审内容",
            value=message['script'],
            placeholder="加载内容...",
            height=600
        )

    # push button
    if st.button(label="推送", type="primary"):
        push_msg = {
            "script": txt,
            "role": message['role'],
            "track": message['track']
        }
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=queue_host))
        channel = connection.channel()
        channel.queue_declare(queue=push_topic)
        channel.basic_publish(exchange='',
                            routing_key=push_topic,
                            body=json.dumps(push_msg))
        connection.close()
        # log
        # print(push_msg)
        # del file
        os.remove(os.path.join(path, files[0]))
        st.rerun()

    # push button
    if st.button(label="跳过"):
        # del file
        os.remove(os.path.join(path, files[0]))
        st.rerun()
