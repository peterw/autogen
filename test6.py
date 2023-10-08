from PIL import Image, ImageDraw, ImageFont
from IPython import get_ipython
import autogen
from dotenv import load_dotenv
import os
import openai
load_dotenv()
# Get the API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set the API key
openai.api_key = OPENAI_API_KEY

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo"],
    },
)

llm_config = {
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
}

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get(
        "content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

# the assistant receives a message from the user, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message="""
find the cutest golden retreiver image and use that image to generate a html page for bob,
and write a birthday poem in the style of kanye west
""",
)
