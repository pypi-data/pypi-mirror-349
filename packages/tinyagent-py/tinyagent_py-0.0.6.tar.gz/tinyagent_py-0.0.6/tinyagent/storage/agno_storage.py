import asyncio
from typing import Dict, Any, Optional
try:
    from tinyagent.storage.base import Storage
    from agno.storage.postgres import PostgresStorage as AgnoPG
    from agno.storage.sqlite import SqliteStorage as AgnoSL
    from agno.storage.session.agent import AgentSession
except ImportError as e:
    raise ImportError("agno is not installed. Please install it with `pip install agno`.", e)

def _remap_agno_to_tiny(ag: Dict[str, Any]) -> Dict[str, Any]:
    """Map a full Agno to_dict() into TinyAgent’s to_dict() shape."""
    sess_id = ag.get("session_id", "")

    # meta = everything except the session_state fields
    metadata = {
        k: v
        for k, v in ag.items()
        if k not in ("session_id", "session_data", "memory", "runs")
    }

    # Safe‐guard: use {} if any of these are None
    _session_data = ag.get("session_data") or {}
    _memory       = ag.get("memory") or {}
   

    session_state = {
        "messages": _memory.get("messages", []),
        "memory":   _memory,
        **_session_data,
    }

    return {
        "session_id": sess_id,
        "metadata": metadata,
        "session_state": session_state,
    }

def _remap_tiny_to_agno(tiny: Dict[str, Any]) -> Dict[str, Any]:
    """
    Given TinyAgent.to_dict() output:
      { "session_id": str,
        "metadata": {...},
        "session_state": { "messages": [...], "memory": {...}, "runs": [...] }
      }
    produce a full AgnoSession.to_dict() shape:
      { "session_id":..., "user_id":..., "memory":..., "runs":...,
        "session_data": {"messages": [...]},
        "extra_data":...,
         ... (other Agno fields remain None/default) }
    """
    session_id = tiny["session_id"]
    meta       = tiny.get("metadata", {}) or {}
    state      = tiny.get("session_state", {}) or {}

    return {
        "session_id":      session_id,
        "user_id":         meta.get("user_id"),
        "team_session_id": meta.get("team_session_id"),
        "memory":          state.get("memory", {}),
        "runs":            state.get("runs", []),
        "session_data":    {"messages": state.get("messages", [])},
        "extra_data":      meta.get("extra_data"),
        # created_at/updated_at/agent_id/agent_data will default in AgnoSession
    }


class AgnoPostgresStorage(Storage):
    def __init__(self, table_name: str, db_url: str, schema: str = "ai", mode: str = "agent"):
        super().__init__()
        self.backend = AgnoPG(table_name=table_name, schema=schema, db_url=db_url, mode=mode)
        self.backend.create()

    async def save_session(self, session_id: str, data: Dict[str, Any], user_id: Optional[str] = None) -> None:
        # Pack TinyAgent dict into AgnoSession record
        agno_dict = _remap_tiny_to_agno(data)
        session_obj = AgentSession.from_dict(agno_dict)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.backend.upsert, session_obj)

    async def load_session(self, session_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        loop = asyncio.get_event_loop()
        agno_obj = await loop.run_in_executor(None, self.backend.read, session_id, user_id)
        if not agno_obj:
            return {}
        ag = agno_obj.to_dict()
        return _remap_agno_to_tiny(ag)

    async def close(self) -> None:
        pass


class AgnoSqliteStorage(Storage):
    def __init__(self, table_name: str, db_url: str, mode: str = "agent"):
        super().__init__()
        self.backend = AgnoSL(table_name=table_name, db_url=db_url, mode=mode)
        self.backend.create()

    async def save_session(self, session_id: str, data: Dict[str, Any], user_id: Optional[str] = None) -> None:
        agno_dict = _remap_tiny_to_agno(data)
        session_obj = AgentSession.from_dict(agno_dict)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.backend.upsert, session_obj)

    async def load_session(self, session_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        loop = asyncio.get_event_loop()
        agno_obj = await loop.run_in_executor(None, self.backend.read, session_id, user_id)
        if not agno_obj:
            return {}
        ag = agno_obj.to_dict()
        return _remap_agno_to_tiny(ag)

    async def close(self) -> None:
        pass