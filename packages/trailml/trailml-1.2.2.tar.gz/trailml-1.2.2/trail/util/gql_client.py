import asyncio
from queue import Queue
from threading import Thread


from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from trail.libconfig import libconfig
from trail.userconfig import userconfig
from trail.util import auth


def build_gql_client():
    return GQLClientWrapper()


class GQLClientWrapper:
    def __init__(self):
        transport = AIOHTTPTransport(
            url=libconfig.gql_endpoint_url(userconfig().endpoint_url),
            headers=auth.build_auth_header(userconfig().api_key, userconfig().email),
        )
        self.client = Client(transport=transport, execute_timeout=30)

    def _run_async_in_thread(self, query, variable_values, result_queue):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def run():
            async with self.client as session:
                try:
                    result = await session.execute(
                        gql(query), variable_values=variable_values
                    )
                    result_queue.put(result)
                except Exception as e:
                    result_queue.put(e)

        loop.run_until_complete(run())
        loop.close()

    def execute(self, query, variable_values=None):
        result_queue = Queue()
        thread = Thread(
            target=self._run_async_in_thread,
            args=(query, variable_values, result_queue),
        )
        thread.start()
        thread.join()
        res = result_queue.get()
        if isinstance(res, Exception):
            raise res
        return res
