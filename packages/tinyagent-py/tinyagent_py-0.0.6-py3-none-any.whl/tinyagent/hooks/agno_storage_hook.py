try:
    import agno
    from agno.storage.postgres import PostgresStorage
    from agno.storage.sqlite import SqliteStorage
    from agno.storage.session.agent import AgentSession
except ImportError as e:
    raise ImportError("agno is not installed. Please install it with `pip install agno`.", e)

import asyncio
from typing import Optional
from agno.storage.postgres import PostgresStorage
from agno.storage.sqlite import SqliteStorage
from agno.storage.session.agent import AgentSession

class PostgresStorageHook:
    def __init__(
        self,
        table_name: str,
        db_url: Optional[str] = None,
        db_engine=None,
        schema: Optional[str] = "ai",
        schema_version: int = 1,
        auto_upgrade_schema: bool = True,
        mode: str = "agent",
    ):
        self.storage = PostgresStorage(
            table_name=table_name,
            db_url=db_url,
            db_engine=db_engine,
            schema=schema,
            schema_version=schema_version,
            auto_upgrade_schema=auto_upgrade_schema,
            mode=mode,
        )

    async def __call__(self, event_name: str, agent, **kwargs):
        if event_name == "agent_start":
            # Load session from storage
            session_id = getattr(agent, "session_id", None)
            user_id = getattr(agent, "user_id", None)
            if session_id:
                session = self.storage.read(session_id=session_id, user_id=user_id)
                if session:
                    # Populate agent state from session
                    agent.messages = session.session_data.get("messages", [])
                    agent.memory = session.memory
                    agent.metadata = session.extra_data
                    # You may need to adapt this depending on tinyagent's state structure

        elif event_name in ("llm_end", "agent_end"):
            # Save session to storage
            session_id = getattr(agent, "session_id", None)
            user_id = getattr(agent, "user_id", None)
            if session_id:
                # Create AgentSession from agent state
                session_data = {
                    "messages": getattr(agent, "messages", []),
                }
                session = AgentSession(
                    session_id=session_id,
                    user_id=user_id,
                    memory=getattr(agent, "memory", {}),
                    session_data=session_data,
                    extra_data=getattr(agent, "metadata", {}),
                    agent_id=getattr(agent, "agent_id", None),
                    team_session_id=None,
                    agent_data=None,
                )
                await asyncio.to_thread(self.storage.upsert, session)

class SqliteStorageHook:
    def __init__(
        self,
        table_name: str,
        db_url: Optional[str] = None,
        db_file: Optional[str] = None,
        db_engine=None,
        schema_version: int = 1,
        auto_upgrade_schema: bool = True,
        mode: str = "agent",
    ):
        self.storage = SqliteStorage(
            table_name=table_name,
            db_url=db_url,
            db_file=db_file,
            db_engine=db_engine,
            schema_version=schema_version,
            auto_upgrade_schema=auto_upgrade_schema,
            mode=mode,
        )

    async def __call__(self, event_name: str, agent, **kwargs):
        if event_name == "agent_start":
            # Load session from storage
            session_id = getattr(agent, "session_id", None)
            user_id = getattr(agent, "user_id", None)
            print("Session ID",session_id)
            print("User ID",user_id)
            if session_id:
                session = self.storage.read(session_id=session_id, user_id=user_id)
                print(f"Session: {session}")
                if session:
                    # Populate agent state from session
                    agent.messages = session.memory.get("messages", [])
                    agent.memory = session.memory
                    agent.metadata = session.extra_data

        elif event_name in ("llm_end", "agent_end"):
            # Save session to storage
            print("Agent metadata",getattr(agent, "metadata", {}))
            session_id = getattr(agent, "session_id", None)
            user_id = getattr(agent, "user_id", None)
            if session_id:
                session_data = {
                    "messages": getattr(agent, "messages", []),
                }
                session = AgentSession(
                    session_id=session_id,
                    user_id=user_id,
                    memory=getattr(agent, "memory", {}),
                    session_data=session_data,
                    extra_data=getattr(agent, "metadata", {}),
                    agent_id=getattr(agent, "agent_id", None),
                    team_session_id=None,
                    agent_data=None,
                )
                await asyncio.to_thread(self.storage.upsert, session)

