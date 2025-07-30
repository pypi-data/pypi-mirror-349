"""
.. include:: ../../../README.md
"""
# Imports in this file affect import paths and documentation

import logging

from remotivelabs.topology import (
    args,
    behavioral_model,
    broker,
    control,
    frame,
    mock,
    namespace,
    namespaces,
    secoc,
    signal,
    some_ip,
    testing,
    time,
)
from remotivelabs.topology.args import ArgvParams
from remotivelabs.topology.behavioral_model import BehavioralModel
from remotivelabs.topology.broker.client import BrokerClient
from remotivelabs.topology.broker.restbus import FrameConfig, SignalConfig
from remotivelabs.topology.frame import Frame, FrameInfo, FrameName, FrameSubscription
from remotivelabs.topology.namespace import NamespaceInfo, NamespaceName
from remotivelabs.topology.namespaces import CanNamespace, GenericNamespace, SomeIPNamespace, filters
from remotivelabs.topology.namespaces.generic import RestbusConfig
from remotivelabs.topology.secoc import SecocCmac0, SecocFreshnessValue, SecocKey, SecocTimeDiff
from remotivelabs.topology.signal import Signal, SignalInfo, SignalName, SignalValue, WriteSignal
from remotivelabs.topology.some_ip import (
    ErrorReturnCode,
    RequestType,
    ReturnCode,
    SomeIPError,
    SomeIPEvent,
    SomeIPRequest,
    SomeIPRequestNoReturn,
    SomeIPRequestReturn,
    SomeIPResponse,
)
from remotivelabs.topology.time.async_ticker import OnTickCallback, create_ticker

# Disable library logging by default
_logger = logging.getLogger("remotivelabs.topology")
_logger.addHandler(logging.NullHandler())

__all__ = [
    "behavioral_model",
    "broker",
    "mock",
    "namespaces",
    "namespace",
    "frame",
    "signal",
    "secoc",
    "some_ip",
    "control",
    "testing",
    "time",
    "args",
]
