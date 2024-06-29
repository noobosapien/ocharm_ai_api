from dotenv import load_dotenv
from handlers.chat_model_start_handler import ChatModelStartHandler
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage
from langchain_openai.chat_models import ChatOpenAI
from memories.sql_history import SQLMessageHistory
from tools.sql import describes_tables_tool, list_tables, run_query_tool

load_dotenv()


class Assistant:
    def __init__(self):
        self.tables = list_tables()
        self.handler = ChatModelStartHandler()
        self.chat = ChatOpenAI(callbacks=[self.handler])

        self.prompt = ChatPromptTemplate(
            messages=[
                SystemMessage(
                    content=(
                        "You are an AI that has access to a PostgresSQL database.\n"
                        f"The database has tables of: {self.tables}\n"
                        "DO NOT MAKE ANY ASSUMPTIONS ABOUT WHAT TABLES EXIST "
                        "OR WHAT COLUMNS EXIST. INSTEAD USE THE 'describe_tables' function"
                    )
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            output_key="answer",
            return_messages=True,
            chat_memory=SQLMessageHistory(conversation_id=1),
            k=4,
        )

        self.agent = OpenAIFunctionsAgent(
            llm=self.chat,
            prompt=self.prompt,
            tools=[run_query_tool, describes_tables_tool],
        )

        self.agent_executor = AgentExecutor(
            agent=self.agent,
            verbose=True,
            tools=[run_query_tool, describes_tables_tool],
            memory=self.memory,
        )

    def call_assistant(self, query):
        return self.agent_executor(query)
