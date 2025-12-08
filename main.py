from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from tools.sql import run_sqlite_query, list_tables, describe_tables

load_dotenv()

chat = ChatOpenAI()

tables = list_tables()

tools = [run_sqlite_query, describe_tables]

system_message = SystemMessage(
    content=f"You are an AI that has access to a SQLite database.\n{tables}"
)

agent = create_agent(
    model=chat,
    tools=tools,
)

result = agent.invoke({"messages": [HumanMessage(content="How many users have provided a shipping address ?")]})

print(result["messages"][1].tool_calls[0]['args'])
print(result["messages"][-1].content)