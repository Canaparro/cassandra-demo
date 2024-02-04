from cassandra.cluster import Session
from cassandra.cqlengine import connection

DATABASE = None

def setup_database() -> Session:
    connection.setup(["127.0.0.1"], "clqengine", protocol_version=3)
    print(connection.DEFAULT_CONNECTION)
    return connection.session

def get_database_connection() -> Session:
    global DATABASE
    if not DATABASE:
        DATABASE = setup_database()
    return DATABASE
