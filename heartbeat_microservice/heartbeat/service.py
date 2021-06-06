"""[Docstring] Declares functions, running the heartbeat."""
import time
from paho.mqtt.client import Client, MQTTMessage
from .heartbeat import Heartbeat


class Service:
    """[Docstring] Static class, holding and managing the microservice's heartbeat thread."""

    heartbeatThread: Heartbeat

    @staticmethod
    def initiateHeartbeat(interval: float, count: int, brokerAddress: str, brokerPort: int, brokerUsername: str, brokerPassword: str, brokerChannel: str):
        """[Docstring] Declares functions, initiating new heartbeat with respective values."""
        Service.heartbeatThread = Heartbeat(interval, count, brokerAddress, brokerPort, brokerUsername, brokerPassword, brokerChannel)
        return Service.heartbeatThread.start()

    @staticmethod
    def stopHeartbeat():
        """[Docstring] Declares functions, stopping currently running heartbeats."""
        return Service.heartbeatThread.stop()

    @staticmethod
    def monitorHeartBeat():
        """[Docstring] Declares functions, fetching current heartbeat count."""
        return Service.heartbeatThread.getCount()
