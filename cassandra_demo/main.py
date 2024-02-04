import asyncio

from database.migrations import migrate_tables


async def main_program():
    Client.create(client_id="first_client", account_id="account_1", name="Marcelo")
    Client.create(client_id="first_client", account_id="account_2", name="Nicole")
    Client.create(client_id="second_client", account_id="account_1", name="Joao Pedro")
    Client.create(client_id="second_client", account_id="account_2", name="Joao Victor")

    results = Client.async_query()
    async for row in results:
        print(row)


if __name__ == "__main__":
    migrate_tables()
    from repository.client import Client
    asyncio.run(main_program())
