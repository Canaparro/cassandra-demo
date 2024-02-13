from cassandra.cqlengine.columns import Text
from database import get_database_connection
from repository.async_base_model import AsyncBaseModel


class Client(AsyncBaseModel):
    __keyspace__ = "social_media"
    client_id = Text(primary_key=True)
    account_id = Text(primary_key=True)
    name = Text()


    @classmethod
    def _session(cls):
        return get_database_connection()
