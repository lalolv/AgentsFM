from langchain.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


class TranslateTools():

    @tool("Translate proper noun")
    def translate_proper_nouns(query):
        """Used to translate proper nouns and return relevant results."""
        api_wrapper = WikipediaAPIWrapper(lang='zh')
        return api_wrapper.run(query)
