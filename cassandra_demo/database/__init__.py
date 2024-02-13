from cassandra.cluster import Session
from cassandra.cqlengine import connection

DATABASE = None

def setup_database() -> Session:
    connection.setup(["127.0.0.1"], "clqengine", protocol_version=4)
    return connection.session

def get_database_connection() -> Session:
    global DATABASE
    if not DATABASE:
        DATABASE = setup_database()
        create_keyspace(DATABASE)
    return DATABASE


def create_keyspace(database: Session):
    keyspace_query = """
            CREATE KEYSPACE IF NOT EXISTS social_media
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
        """
    database.execute(keyspace_query)
