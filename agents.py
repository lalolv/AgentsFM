from crewai import Agent
from textwrap import dedent
from langchain.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun

tavily_search_tool = TavilySearchResults()
ddg_search_tool = DuckDuckGoSearchRun()

# This is an example of how to define custom agents.
# You can define as many agents as you want.
# You can also define custom tasks in tasks.py
class FMAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(
            model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        self.Ollama = Ollama(model="openhermes")

    def researcher(self):
        return Agent(
            role="Popular Music Investigator",
            backstory=dedent(f"""You work for a leading music radio station.
                Your speciality is identifying emerging trends.
                You are adept at spotting information on the cutting edge of popular music and
                identifying artist-related news stories and gossip."""),
            goal=dedent(f"""Explore international popular music trends"""),
            tools=[ddg_search_tool, tavily_search_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT35,
        )
