import os
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import json
from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import UserProxyAgent
import autogen


load_dotenv()
browserless_api_key = os.getenv("BROWSERLESS_API_KEY")
serper_api_key = os.getenv("SERP_API_KEY")
airtable_api_key = os.getenv("AIRTABLE_API_KEY")
config_list = config_list_from_json("OAI_CONFIG_LIST")



# Create functions ------------------ #

# Create agents --------------------- #

# Create user proxy agent
user_proxy = UserProxyAgent(name="user_proxy",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=1
    )

# Create thesis agent
researcher = GPTAssistantAgent(
    name = "researcher",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_tR7vKzX9EdLvyIhWulBxBBbF"
    }
)
# Create researcher agent
researcher = GPTAssistantAgent(
    name = "researcher",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_tR7vKzX9EdLvyIhWulBxBBbF"
    }
)


# Create research manager agent
research_manager = GPTAssistantAgent(
    name="research_manager",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_fiaO05ykmux5zCb8H6DH78Uw"
    }
)


# Create director agent
director = GPTAssistantAgent(
    name = "director",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_lmIXGArilTLIG25f52ITOiio"
    }
)

# Create group chat ------------------ #

# Create group chat
groupchat = autogen.GroupChat(agents=[user_proxy, researcher, research_manager, director], messages=[], max_round=15)
group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})


# Start conversation ------------------ #
message =""
user_proxy.initiate_chat(group_chat_manager, message=message)
#user_proxy.initiate_chat(researcher, message=message)