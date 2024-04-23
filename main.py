
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

from textwrap import dedent
from agents import FMAgents
from tasks import FMTasks

# This is the main class that you will use to define your custom crew.
# You can define as many agents and tasks as you want in agents.py and tasks.py


class FMCrew:
    def __init__(self, title, artist, album):
        self.title = title
        self.artist = artist
        self.album = album

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = FMAgents()
        tasks = FMTasks()

        # Define your custom agents and tasks here
        researcher = agents.researcher()

        # Custom tasks include agent name and variables as input
        lookup_track_info = tasks.lookup_track_info(
            researcher,
            self.title,
            self.artist,
            self.album
        )

        # Define your custom crew here
        crew = Crew(
            agents=[researcher],
            tasks=[lookup_track_info],
            verbose=True,
        )

        result = crew.kickoff()
        return result


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to FM AI Agents")
    print("-------------------------------")
    

    # Title: The Conflict of the Mind
    # Artist: AURORA
    # Album: The Conflict of the Mind
    title = input(dedent("""Enter Title: """))
    artist = input(dedent("""Enter Artist: """))
    album = input(dedent("""Enter Album: """))

    fm_crew = FMCrew(title, artist, album)
    result = fm_crew.run()
    print("\n\n########################")
    print("## Here is fm crew run result:")
    print("########################\n")
    print(result)
