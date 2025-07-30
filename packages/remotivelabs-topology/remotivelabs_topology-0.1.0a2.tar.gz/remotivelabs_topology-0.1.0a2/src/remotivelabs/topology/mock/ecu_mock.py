from __future__ import annotations

import asyncio
import logging
from contextlib import AsyncExitStack

from remotivelabs.topology.behavioral_model import BehavioralModel
from remotivelabs.topology.broker.client import BrokerClient
from remotivelabs.topology.mock.args import ECUMockArgs
from remotivelabs.topology.namespaces import filters
from remotivelabs.topology.namespaces.generic import GenericNamespace, RestbusConfig

_log = logging.getLogger(__name__)


class ECUMock:
    def __init__(self, args: ECUMockArgs):
        self._namespaces = args.namespaces
        self._broker_url = args.broker_url
        self._delay_multiplier = args.delay_multiplier

    async def run(self):
        async with BrokerClient(self._broker_url) as broker_client:
            models: list[BehavioralModel] = [
                BehavioralModel(
                    ecu,
                    namespaces=[
                        GenericNamespace(
                            name=namespace,
                            broker_client=broker_client,
                            restbus_configs=[RestbusConfig([filters.Sender(ecu_name=ecu)])],
                        )
                        for namespace in namespace_list
                    ],
                    broker_client=broker_client,
                )
                for ecu, namespace_list in self._namespaces.items()
            ]

            async with AsyncExitStack() as stack:
                for model in models:
                    await stack.enter_async_context(model)
                await asyncio.gather(*(model.run_forever() for model in models))
