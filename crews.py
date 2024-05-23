from crewai import Crew, Process
from agents import FMAgents
from tasks import FMTasks

class FMCrew:
    def __init__(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        self.agents = FMAgents()
        self.tasks = FMTasks()

    def explore_music(self, title, artist, album):
        # Define your custom agents and tasks here
        researcher = self.agents.research_agent()
        analyst = self.agents.music_analyst()
        writer = self.agents.scripts_content_writer()

        # 收集参考信息
        gather_task = self.tasks.gather_task(
            researcher,
            title,
            artist,
            album
        )
        # 撰写脚本
        draft_scripts = self.tasks.draft_scripts(
            writer,
            title,
            artist,
            album
        )

        # Define your custom crew here
        crew = Crew(
            agents=[researcher, analyst, writer],
            tasks=[gather_task, draft_scripts],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        return result

    # 抓取新闻，并保存到文件中
    def broadcasting_news(self, title: str, content: str, link:str):
        # Define your custom agents and tasks here
        researcher = self.agents.research_agent()
        writer = self.agents.scripts_content_writer()
        translator = self.agents.translator()

        # 总结新闻
        # summarize_news = self.tasks.summarize_news(researcher, link, content)
        # 撰写脚本
        draft_scripts = self.tasks.draft_news_scripts(writer, title, link, content)
        # 翻译
        # translate_scripts = self.tasks.translate_scripts(translator)

        # Define your custom crew here
        crew = Crew(
            agents=[writer],
            tasks=[draft_scripts],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        return result
