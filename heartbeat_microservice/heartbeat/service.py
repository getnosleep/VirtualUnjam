"""[Docstring] Declares functions, running the heartbeat."""
from .publisher import Publisher
from .heartbeat import Heartbeat


class Service:
    """[Docstring] Static class, holding and managing the microservice's heartbeat thread."""

    heartbeatThread: Heartbeat

    @staticmethod
    def initiateHeartbeat(interval: float, count: int, publisher: Publisher):
        """[Docstring] Declares functions, initiating new heartbeat with respective values."""
        Service.heartbeatThread = Heartbeat(interval, count, publisher)
        return Service.heartbeatThread.start()

    @staticmethod
    def stopHeartbeat():
        """[Docstring] Declares functions, stopping currently running heartbeats."""
        return Service.heartbeatThread.stop()

    @staticmethod
    def monitorHeartBeat():
        """[Docstring] Declares functions, fetching current heartbeat count."""
        return Service.heartbeatThread.getCount()
