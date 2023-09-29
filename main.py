from autogen import AssistantAgent, UserProxyAgent
import autogen

config_list_gpt4 = [{
    "model": "gpt-4",
    "api_key": "<OPENAI_API_KEY>"
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
fun_engineer = autogen.AssistantAgent(
    name="Fun_Manager",
    llm_config=gpt4_config,
    system_message='''Fun Manager. You maximize the fun when Admin is at a location - optimize for unique memorable experiences & fun stories.
''',
)

gym_trainer = autogen.AssistantAgent(
    name="Gym_Trainer",
    llm_config=gpt4_config,
    system_message='''Gym Trainer. You make sure admin is getting the right training (lifting 4-5 times a week) and eating the right food to get to a 6-pack. 
''',
)
exectuvie_assistant = autogen.AssistantAgent(
    name="Executive_Assistant",
    llm_config=gpt4_config,
    system_message="""Executive Assistant. You make sure the daily work (like project deadlines & daily habits like design and copywriting practice) required by the Admin is done before any of the fun activities."""
)

planner = autogen.AssistantAgent(
    name="Planner",
    system_message='''Planner. Suggest a plan. Revise the plan based on feedback from admin, Executive Assistant, Fun Manager, until admin approval.
Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
''',
    llm_config=gpt4_config,
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, make sure all objectives from fun manager, executive assistant, and gym trainer are met. provide feedback.",
    llm_config=gpt4_config,
)

groupchat = autogen.GroupChat(agents=[
                              user_proxy, fun_engineer, exectuvie_assistant, gym_trainer, planner, critic], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

user_proxy.initiate_chat(
    manager,
    message="""
plan a month long trip to bangkok. include a table of dates and activity. i will give you a list of tasks that need to be done in a particular day
""",
)
