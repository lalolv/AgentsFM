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
from tools.translate_tool import TranslateTools


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
        # self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        # self.AzureOpenAI = AzureChatOpenAI()
        # self.Gemini = GoogleGenerativeAI(
        #     model="gemini-1.5-flash", google_api_key=os.getenv('GEMINI_KEY'))
        # self.Ollama = Ollama(model="llama3:instruct")
        self.Qwen = Ollama(model="qwen:14b-chat")
        # self.Yi = Ollama(model="yi:9b-v1.5")
        # GROP, 30 RPM; 14,400 RPD; 
        # mixtral-8x7b-32768 5,000 TPM
        # llama3-70b-8192 6,000 TPM
        self.Groq = ChatGroq(temperature=0.7, model_name="llama3-70b-8192")

    def research_agent(self):
        return Agent(
            role="Information Investigator",
            backstory=dedent(
            f"""
                Known as the BEST information investigator.
                Your specialty is identifying emerging trends. 
                You are adept at collecting, interpreting and summarizing this cutting-edge information.
            """),
            goal=dedent(f"""Provide reference information"""),
            tools=[scrape_search_tool, ddg_search_tool,
                   wikipedia_tool, tavily_search_tool],
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
            llm=self.Qwen,
            max_iter=6
        )

    # With a keen eye for detail and a passion for storytelling,
    # you have refined scripts for DJ,
    # turning bland text into engaging stories.
    # Get valuable information from **Information Investigator**,
    def scripts_content_writer(self):
        return Agent(
            role="Scripts Content Writer",
            backstory=dedent(f"""
                You're a professional writer,
                You have a keen eye for detail and a passion for storytelling.
                Turn bland words into compelling stories.
            """),
            goal=dedent(f"""Write a summary paragraph in Chinese"""),
            tools=[wikipedia_tool],
            allow_delegation=False,
            verbose=True,
            llm=self.Qwen,
            max_iter=6,
            max_rpm=30,
            memory=False,
            max_execution_time=None
        )
    
    # WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang='en'))
    def translator(self):
        return Agent(
            role="translator",
            backstory=dedent(f"""您是一个专业的中文翻译员，可以把任何语言翻译为简体中文。
                根据 **Scripts Content Writer** 提供的最终内容，翻译为语义连贯、通顺、优美、优雅且高级的中文词汇和语句。
                保持意思相同，但使其更具文学性。
            """),
            goal=dedent(f"""把内容翻译为简体中文"""),
            allow_delegation=False,
            verbose=True,
            llm=self.Qwen,
            max_iter=2,
            max_rpm=2,
            memory=False,
            max_execution_time=None
        )
