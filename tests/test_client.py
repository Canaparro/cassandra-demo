import os
from unittest import IsolatedAsyncioTestCase

from cassandra.cqlengine.management import sync_table
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from cassandra_demo.repository.client import Client
from database import get_database_connection


class TestClient(IsolatedAsyncioTestCase):


    @classmethod
    def setUpClass(cls):
        # os.environ["DOCKER_HOST"] = 'unix:///home/canaparro/.docker/desktop/docker.sock'
        cls.cassandra = DockerContainer("cassandra").with_bind_ports(9042, 9042)
        cls.cassandra.start()
        wait_for_logs(cls.cassandra, "Startup complete")

    @classmethod
    def tearDownClass(cls):
        cls.cassandra.stop()

    def setUp(self):
        session = get_database_connection()
        session.execute(f"DROP TABLE IF EXISTS {Client._get_keyspace()}.{Client._raw_column_family_name()}")
        sync_table(Client)

    def tearDown(self):
        pass


    async def test_given_a_client_when_saving_should_persist_it(self):
        client = Client(client_id="1", account_id="2", name="some_name")
        client.save()
        result = Client.async_query()
        final_result = [row async for row in result]
        self.assertEqual(final_result, [client])

    async def test_given_a_client_when_saving_should_persist_it2(self):
        client = Client(client_id="1", account_id="2", name="some_name")
        client.save()
        result = Client.async_query()
        final_result = [row async for row in result]
        self.assertEqual(final_result, [client])
