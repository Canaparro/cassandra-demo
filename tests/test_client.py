from time import sleep

from cassandra_demo.repository.client import Client

# from cassandra_demo.database.migrations import migrate_tables
from tests.base_cassandra_test import CassandraTest


class TestClient(CassandraTest):

    async def test_given_a_client_when_saving_should_persist_it(self):

        client = Client(client_id="1", account_id="2", name="some_name")
        client.save()
        result = Client.async_query()
        final_result = [row async for row in result]
        self.assertEqual(final_result, [client])
