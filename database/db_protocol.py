from typing import Protocol, Any

class Database(Protocol):
    def execute(self, query: str, params: tuple = ()) -> Any: 
        ... # It says no implementation here. we could also use 'pass' but '...' (Ellipsis) this is standard when we work with protocols
    def fetchall(self) -> list: 
        ...
    def commit(self) -> None: 
        ...
    @property
    def lastrowid(self) -> int: 
        ...
