from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from tools.sql import run_sqlite_query

load_dotenv()

chat = ChatOpenAI()

system_prompt = SystemMessage(content="You are a database query assistant.")

tools = [run_sqlite_query]

agent = create_agent(
    model=chat,
    tools=tools,
    system_prompt=system_prompt,
)

result = agent.invoke({"messages": [HumanMessage(content="How many users are in the database?")]})

print(result["messages"][-1].content)