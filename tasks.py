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
                    请使用简短的文案，总结、概括和解读下面的关键内容内容。
                    {web}

                    确保尽可能为 Scripts Content Editor 提供最新的、最有价值的参考信息。
                """
            ),
            expected_output="总结一个段落，告诉听众一些最新的有价值的新闻资讯",
            agent=agent,
        )
    
    def summarize_news(self, agent, link: str, content: str):
        return Task(
            description=dedent(
                f"""
                    Interpret, analyze and summarise the key points of the following article content (or URL):
                    > {content}
                    >
                    > **URL** {link}
                """
            ),
            expected_output="A summary paragraph",
            agent=agent,
        )
    
    def summarize_feed(self, agent, link:str, content:str):
        return Task(
            description=dedent(
                f"""
                    请使用简体中文，解读并总结以下文章内容（或网页链接）的主要观点：
                    > {content}
                    >
                    > **网页链接** {link}
                """
            ),
            expected_output="编写一篇总结性的文案",
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
    # tick-tock
    # 2. The final content of the copy must be in **plain text format ** 
    # and not contain characters or markup in other formats, such as Markdown。
    def draft_news_scripts(self, agent, title:str, link:str, content:str):
        return Task(
            description=dedent(
                f"""
                ## Task Description
                - Interpret, analyze and summarise the key points of the following content (or URL).
                - Knowledge and some ideas are presented in a light, pleasant, humorous and chatty tone.
                - Try to keep the original point of view and content.
                - Written in semantically coherent, fluent, elegant, and advanced **Simplified Chinese**.
                - Keep the meaning the same, but make it more literary.

                ----

                > Title: {title}
                > Content: {content}
                > URL: {link}

                ----

                ## Notes
                1. Don't include redundant prompts，example:
                - Notice ...
                - Note ...
                - etc.
                2. The final copy content, which must be in plain text format, 
                should not contain characters from other formats, such as Markdown.

                {self.__tip_section()}
                """
            ),
            expected_output="A coherent and amazing plain Chinese text, up to 3000 words",
            agent=agent
        )

    def translate_scripts(self, agent):
        return Task(
            description=dedent(
            f"""
                把最终答案，翻译为简体中文。

                {self.__tip_section()}
                """
            ),
            expected_output="一段以中文为主要语言的文本",
            agent=agent
        )
