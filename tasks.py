from crewai import Task
from textwrap import dedent


# This is an example of how to define custom tasks.
# You can define as many tasks as you want.
# You can also define custom agents in agents.py
class FMTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def lookup_news(self, agent, web):
        return Task(
            description=dedent(
                f"""
                    请使用简短的文案，总结和概括下面资讯页面的核心内容。
                    {web}

                    确保尽可能为 Scripts Content Editor 提供最新的、最有价值的参考信息。
                """
            ),
            expected_output="总结一个段落，告诉听众一些最新的有价值的新闻资讯",
            agent=agent,
        )
    
    def summarize_news(self, agent, content):
        return Task(
            description=dedent(
                f"""
                    Summarize and analyze the key points of the content：
                    {content}
                """
            ),
            expected_output="Summarize a paragraph that tells the audience something new and valuable.",
            agent=agent,
        )

    def gather_task(self, agent, title, artist, album):
        return Task(
            description=dedent(
                f"""
                    考虑从以下几个方面，收集参考信息：
                    - 有关流行音乐、音乐表演和音乐活动的最新事件和新闻（可以使用关键词 "{artist} - {title}" 搜索）。
                    - 搜索最新的科技新闻，比如: 信息技术、人工智能（AI）等。
                    - 查询最新的游戏资讯，如: 新游戏、更新动态等。

                    您只能从上面的这些中，选择其中一个方面收集信息，如果找不到合适的，可以再重新选择其他方面信息。

                    {self.__tip_section()}

                    确保尽可能为 Scripts Content Editor 提供最新参考信息。
                    以下是下一段要播放的音乐的一些信息：
                    Title: {title}
                    Artist: {artist}
                    Album: {album}
                """
            ),
            expected_output="为编辑提供一些最新的参考信息",
            agent=agent,
        )
    
    def draft_joke(self, agent):
        return Task(
            description=dedent(
                f"""
                    编写 one-liner 风格的脱口秀段子，总是让人捧腹大笑，并且引起人们的反思。
                """
            ),
            expected_output="编写一个简短的段子或笑话",
            agent=agent,
        )
    
    # 脚本内容参考 "Information Investigator" 或 "Music Specialist" 提供的信息。
    def draft_scripts(self, agent, title, artist, album):
        return Task(
            description=dedent(
                f"""
                为电台主持人 DJ，编写一段中文的脚本台词。
                最终的内容可以是新闻资讯或音乐相关的主题内容。
                歌手、专辑名称和歌曲名，这些都使用原来的英文描述。
                
                开头不需要打招呼，可以直奔主题。比如：
                - 来自 {artist} 的歌曲 {title}
                - {artist} 的新歌曲
                - {title} 表达了...
                - 下面是一则新闻...

                最后一句话需要使用主播 DJ 的语气，介绍下一个播放的音乐节目，比如：
                - 下面为您带来一首动感的音乐 {title}
                - 接下来是一首动感的音乐 {title}
                - 跟着音乐的节奏摇摆你的身体！
                - 下面的音乐希望给您带来美好的时光
                - 马上听到是 {artist} 的这首 {title}

                为了方便 DJ 按照原文讲述，最终的文案内容不要包含开始和结束类似标记描述，不含有类似下面的文本：
                - [电台DJ声音]
                - [电台DJ声音结束]

                最终的文案内容，必须是纯文本格式，不要包含其他格式的字符，比如 Markdown。

                {self.__tip_section()}

                以下是下一段要播放的音乐的一些信息：
                Title: {title}
                Artist: {artist}
                Album: {album}
                """
            ),
            expected_output="为主持人DJ编写一段400字内的连续性中文脚本",
            agent=agent
        )
    
    # 脚本内容参考 "Information Investigator" 或 "Music Specialist" 提供的信息。
    def draft_news_scripts(self, agent, title:str):
        return Task(
            description=dedent(
                f"""
                获取 [Information Investigator] 提供的上下文参考信息，
                在尽量保持原文内容不变的基础上，翻译成中文后讲述新闻、资讯、观点或解读。

                标题: {title} 

                可以使用简单的一句话作为结尾，例如：
                - 一段美妙的音乐后，我们继续聊聊有趣的话题。
                - 继续进入音乐的世界，之后带来更加有意思的话题。
                - 放松一下，先听一段动感的音乐。
                - 听一段音乐，休息一下，稍后回来。
                - 动感的音乐之后再继续。您有什么想聊的吗？
                - 音乐不停，话题不断。您还有什么想说的吗？
                - 好了！再次回到音乐的世界，不要走开。

                翻译的时候，需要注意以下几点：
                - AI 翻译为：人工智能
                - Netflix 翻译为：网飞

                不要包含多余的提示信息，如：Notice、Note 等。
                最终的文案内容，必须是纯中文文本格式，不要包含其他格式的字符，比如 Markdown。

                {self.__tip_section()}
                """
            ),
            expected_output="编写一段连续性中文脚本",
            agent=agent
        )
