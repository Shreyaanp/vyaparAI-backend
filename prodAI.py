import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from langchain.tools import Tool, DuckDuckGoSearchResults
from langchain.utilities import SerpAPIWrapper
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, AgentType

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_APIKEY")
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_APIKEY")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36'
}

ddg_search = DuckDuckGoSearchResults()
search = SerpAPIWrapper()

serpapi_tool = Tool(
    name="Search",
    func=search.run,
    description="Useful for when you need to answer questions about current events",
)

def parse_html(content) -> str:
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text()

def fetch_web_page(url: str) -> str:
    response = requests.get(url, headers=HEADERS)
    return parse_html(response.content)

web_fetch_tool = Tool.from_function(
    func=fetch_web_page,
    name="WebFetcher",
    description="Fetches the content of a web page"
)

prompt_template = "Summarize the following content in more or less than 400 words. The content is about a product and we need to generate SEO friendly data: {content}"
llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
llm_chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt_template))
summarize_tool = Tool.from_function(
    func=llm_chain.run,  # Note: Adjust according to actual function reference.
    name="Summarizer",
    description="Summarizes a web page"
)


tools = [serpapi_tool, web_fetch_tool, summarize_tool]
agent = initialize_agent(
    tools=tools,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    llm=llm,
    verbose=True,
    handle_parsing_errors=True
)

prompt = None

def process_prompt(prompt: str) -> str:
    post_prompt = '''. Use your tools to search and create a proper product name, product description, about product in podints, and a product tagline. The output should be in this format :
Product Name: [product name]
Product Description: [product description]
About Product: [about product in points]
Product Tagline: [product tagline]
also generate a SEO friendly data for the product, like tags.
The generated data should be more or less around 400 words.
Do not break the above format.

'''
    prompt = prompt+" "+post_prompt
    return agent.run(prompt)


if __name__ == "__main__":
    # Test processing a prompt
    test_prompt = "Name of the product : intitle:kala namak rice"
    print("Processing Prompt:", test_prompt)
    processed_prompt = process_prompt(test_prompt)
    print("Processed Prompt Result:", processed_prompt)
