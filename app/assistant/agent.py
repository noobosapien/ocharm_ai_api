import traceback

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import (  # noqa
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
)
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage
from langchain_openai.chat_models import ChatOpenAI

from app.assistant.handlers.chat_model_start_handler import (
    ChatModelStartHandler,  # noqa
)
from app.assistant.memories.sql_history import SQLMessageHistory  # noqa
from app.assistant.tools.sql import (  # noqa
    describes_tables_tool,
    list_tables,
    run_query_tool,
)

load_dotenv()


class Assistant:
    def __init__(self, db):
        self.db = db
        self.tables = list_tables(self.db)
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

        # self.memory = ConversationBufferWindowMemory(
        #     memory_key="chat_history",
        #     output_key="answer",
        #     return_messages=True,
        #     chat_memory=SQLMessageHistory(conversation_id=1, db=self.db),
        #     k=4,
        # )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        self.agent = create_openai_functions_agent(
            llm=self.chat,
            tools=[run_query_tool, describes_tables_tool],
            prompt=self.prompt,
        )

        self.agent_executor = AgentExecutor(
            agent=self.agent,
            verbose=False,
            tools=[run_query_tool, describes_tables_tool],
            memory=self.memory,
        )

    def call_assistant(self, query):
        try:
            return self.agent_executor.invoke({"input": query})
        except Exception as e:
            print(e.__traceback__)
            print(traceback.format_exc())
