from crewai import Task
from textwrap import dedent


# This is an example of how to define custom tasks.
# You can define as many tasks as you want.
# You can also define custom agents in agents.py
class FMTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def lookup_track_info(self, agent, title, artist, album):
        return Task(
            description=dedent(
                f"""
                    Search for as much information as possible about the song in its entirety,
                    such as the context in which it was written, Art Philosophy, what the song is trying to say,
                    what the artist has been in the news recently, etc.

                    {self.__tip_section()}

                    Make sure to use the most recent data as possible.
                    Here's some info on the track：
                    Title: {title}
                    Artist: {artist}
                    Album: {album}
                """
            ),
            expected_output="Summarise a paragraph that tells the listener some interesting information",
            agent=agent,
        )
