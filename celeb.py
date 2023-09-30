from autogen import AssistantAgent, UserProxyAgent
import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
    },
)
config_list_gpt4 = [{
    "model": "gpt-4",
    "api_key": "KEY"
}
]
gpt4_config = {
    "seed": 42,  # change the seed for different trials
    "temperature": 0,
    "config_list": config_list_gpt4,
    "request_timeout": 120,
}

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config=False,
)

kanye_west = autogen.AssistantAgent(
    name="Kanye_West",
    llm_config=gpt4_config,
    system_message='''Kanye West. Imagine you are Kanye West, inhereit all of his characterstics, desires, dreams, goals. Talk as if you were them. 
    Give direct quotes that you've said or previous expereinces that you've been through to say what you are saying.
''',
)

elon_musk = autogen.AssistantAgent(
    name="Elon_Musk",
    llm_config=gpt4_config,
    system_message='''Elon Musk. Imagine you are Elon Musk, inhereit all of his characterstics, desires, dreams, goals. Talk as if you were them.
        Give direct quotes that you've said or previous expereinces that you've been through to say what you are saying.
''',
)

charlie_munger = autogen.AssistantAgent(
    name="Charlie_Munger",
    llm_config=gpt4_config,
    system_message='''Charlie Munger. Imagine you are Charlie Munger inhereit all of his characterstics, desires, dreams, goals. Talk as if you were them.
        Give direct quotes that you've said or previous expereinces that you've been through to say what you are saying.
''',
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message='''Critic. Double check plan, make sure all opinions from Kanye West, Elon Musk, Charlie Munger are accounted for.
      Get them to argue the pros and cons of the decisions. Challenge them if they are not backing up why they are saying what they are saying, they need to justify with their previous expereinces
      ''',
    llm_config=gpt4_config,
)

groupchat = autogen.GroupChat(agents=[
                              kanye_west, user_proxy, elon_musk, charlie_munger, critic], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

user_proxy.initiate_chat(
    manager,
    message="""Should I marry my gf before or after I start my startup? 
""",
)
