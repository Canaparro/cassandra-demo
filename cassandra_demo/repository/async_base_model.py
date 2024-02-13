import asyncio
from asyncio.futures import Future

from cassandra.cluster import ResponseFuture, ResultSet, Session
from cassandra.cqlengine.models import Model


class AsyncBaseModel(Model):
    __abstract__ = True

    @classmethod
    async def async_query(cls):
        prepared_statement = cls.prepare_statement()
        cassandra_future: ResponseFuture = cls._session().execute_async(prepared_statement)

        future_response = asyncio.Future()
        cassandra_future.add_errback(cls._exception_handler, future_response)
        cassandra_future.add_callback(
            cls._success_handler,
            future_response,
            cassandra_future,
        )
        result = await future_response
        for row in result:
            yield cls._construct_instance(row)

        # return await future_response

    @classmethod
    def prepare_statement(cls):
        query = f"SELECT * from {cls._get_keyspace()}.{cls._table_name}"
        prepared_statement = cls._session().prepare(query)
        return prepared_statement

    def _success_handler(result, future_response: Future, cassandra_future):
        future_response.get_loop().call_soon_threadsafe(
            future_response.set_result, ResultSet(cassandra_future, result)
        )

    def _exception_handler(exception, future_response: Future):
        future_response.get_loop().call_soon_threadsafe(
            future_response.set_exception, exception
        )
