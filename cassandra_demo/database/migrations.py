from cassandra.cqlengine.management import sync_table
from repository.client import Client


def migrate_tables():
    sync_table(Client)
