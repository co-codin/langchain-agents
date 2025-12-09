from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.memory import ConversationBufferMemory
from tools.report import write_report_tool
from tools.sql import run_sqlite_query, list_tables, describe_tables

load_dotenv()

chat = ChatOpenAI(model="gpt-4.1")

tables = list_tables()

memory = ConversationBufferMemor(memory_key="chat_history", return_messages=True)
tools = [run_sqlite_query, describe_tables, write_report_tool]

system_message = SystemMessage(
    content=f"You are an AI that has access to a SQLite database.\n"
            f"The database has tables of: {tables}\n"
            "Do not make any assumptions about what tables exist "
            "or what columns exist. Instead, use the 'describe_tables' function"
)

agent = create_agent(
    model=chat,
    tools=tools,
    memoryview=memory
)


result = agent.invoke({"messages": [HumanMessage(content="Summarize the top 5 most popular products. Write the results to a report file")]})

print(result["messages"][1].tool_calls[0]['args'])
print(result["messages"][-1].content)