from crewai import Agent
from crewai_tools import ScrapeWebsiteTool
from textwrap import dedent
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.bing_search import BingSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from dotenv import load_dotenv
import os


load_dotenv()

tavily_search_tool = TavilySearchResults()
# bing_search_tool = BingSearchRun()
ddg_search_tool = DuckDuckGoSearchRun()
scrape_search_tool = ScrapeWebsiteTool()
wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang='zh'))

# This is an example of how to define custom agents.
# You can define as many agents as you want.
# You can also define custom tasks in tasks.py


class FMAgents:
    def __init__(self):
        # self.OpenAIGPT35 = ChatOpenAI(
        #     model_name="gpt-3.5-turbo", temperature=0.7)
        # self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        # self.AzureOpenAI = AzureChatOpenAI()
        self.Gemini = GoogleGenerativeAI(
            model="gemini-1.5-flash", google_api_key=os.getenv('GEMINI_KEY'))
        self.Ollama = Ollama(model="llama3:instruct")
        self.Qwen = Ollama(model="qwen:14b-chat")
        self.Yi = Ollama(model="yi:9b-v1.5")
        # GROP, 30 RPM; 14,400 RPD; 
        # mixtral-8x7b-32768 5,000 TPM
        # llama3-70b-8192 6,000 TPM
        self.Groq = ChatGroq(temperature=0.7, model_name="llama3-70b-8192")

    def research_agent(self):
        return Agent(
            role="Information Investigator",
            backstory=dedent(f"""你在一家领先的广播电台工作。您的专长是识别新兴趋势。
                您善于收集、解读、总结并概括这些前沿信息。"""),
            goal=dedent(f"""提供参考信息"""),
            tools=[scrape_search_tool, ddg_search_tool, wikipedia_tool, tavily_search_tool],
            allow_delegation=True,
            verbose=False,
            llm=self.Qwen,
            max_iter=10
        )

    def music_analyst(self):
        return Agent(
            role="Music Specialist",
            backstory=dedent(
                f"""您是一名音乐领域的专家，善于发现音乐创作背景，解读音乐传达出来的艺术理念。"""),
            goal=dedent(
                f"""提供对音乐的见解"""),
            tools=[wikipedia_tool, ddg_search_tool, tavily_search_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.Ollama,
            max_iter=6
        )

    # With a keen eye for detail and a passion for storytelling,
    # you have refined scripts for DJ,
    # turning bland text into engaging stories.
    def scripts_content_editor(self):
        return Agent(
            role="Scripts Content Editor",
            backstory=dedent(f"""您是一个电台的脚本文案编辑，
                使用凭借敏锐的细节观察力和对故事的热情，
                同时您参考 [Information Investigator] 或 [Music Specialist] 提供的有价值的信息，
                可以为主播 DJ 打磨脚本，将平淡的文字变成了引人入胜的故事。
                """),
            goal=dedent(f"""编写一段中文脚本文案"""),
            tools=[wikipedia_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.Groq,
            max_iter=6,
            max_rpm=30,
            memory=False,
            max_execution_time=None
        )
