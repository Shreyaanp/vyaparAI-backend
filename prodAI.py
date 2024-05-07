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

prompt_template = "Summarize the following content in more or less than 400 words. The content is about a product and we need to generate SEO friendly data. Also you have to search the internet for all different names the product is called by in local or regional parts of the world. scrape the internet and find all the names , it could have multiple name and then list them.: {content}"
llm = ChatOpenAI(model="gpt-4-turbo")
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
    post_prompt = '''. Use your tools to search the internet about the product and its aletnate names in local terms in India in english.
      You need to search the internet and find all the different names of the product called in different regions all around India in english, along with the location of the native name using the web search, there can be more than one single name so do not miss the other names. 
    Create a proper product name, product description, about product in points, a product tagline.
    In product description also add the history of the product as well the the benefit of the product with the target as explanation of the product as to why this product should be used. The intension is to display as much information about the product in the most innovative way as possible. The output should be in this format :
Product Name: [product name]
Different names of the Product: [different names of the product(along with the the local area of the native name), another product name(local area of the native name).... and so on]
Product Description: [product description should be minimum 400 words]
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
    test_prompt = "Name of the product : intitle : काला नमक चावल"
    print("Processing Prompt:", test_prompt)
    processed_prompt = process_prompt(test_prompt)
    print("Processed Prompt Result:", processed_prompt)
