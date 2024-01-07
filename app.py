import os
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
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
brwoserless_api_key = os.getenv("BROWSERLESS_API_KEY")
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
thesis_agent = GPTAssistantAgent(
    name = "agent",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_9CCtVElya0beNbhEAw6XdeGf"
    }
)

# Create thesis manager agent
thesis_manager = GPTAssistantAgent(
    name="manager",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_Zk5WNwrE61SiVCuCfA0CBFqi"
    }
)

# Create proofreader agent
proofreader = GPTAssistantAgent(
    name = "proofreader",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_Z4S0aVILsYhBfBCYBGyJBJQO",
    }
)

# Create group chat ------------------ #

# Create group chat
groupchat = autogen.GroupChat(agents=[user_proxy, thesis_agent, thesis_manager, proofreader], messages=[], max_round=15)
group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})


# ------------------ start conversation ------------------ #
message = "Write a chapter with the title Current state of the art of silicon micropumps"
user_proxy.initiate_groupchat(group_chat_manager, message=message)
#user_proxy.initiate_chat(researcher, message=message)