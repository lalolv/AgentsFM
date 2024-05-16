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
        editor = self.agents.scripts_content_editor()

        # 收集参考信息
        gather_task = self.tasks.gather_task(
            researcher,
            title,
            artist,
            album
        )
        # 撰写脚本
        draft_scripts = self.tasks.draft_scripts(
            editor,
            title,
            artist,
            album
        )

        # Define your custom crew here
        crew = Crew(
            agents=[researcher, analyst, editor],
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
        editor = self.agents.scripts_content_editor()

        # 总结新闻
        summarize_feed = self.tasks.summarize_feed(researcher, link, content)
        # 撰写脚本
        draft_scripts = self.tasks.draft_news_scripts(editor, title, link)

        # Define your custom crew here
        crew = Crew(
            agents=[researcher, editor],
            tasks=[summarize_feed, draft_scripts],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        return result
