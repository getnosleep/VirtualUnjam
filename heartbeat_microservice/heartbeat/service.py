"""[Docstring] Declares functions, running the heartbeat."""
from .heartbeat import Heartbeat


class Service:
    """[Docstring] Static class, holding and managing the microservice's heartbeat thread."""

    heartbeatThread: Heartbeat

    @staticmethod
    def initiateHeartbeat(interval: float, count: int, brokerAddress: str, brokerPort: int, brokerUsername: str, brokerPassword: str, brokerChannel: str) -> bool:
        """[Docstring] Declares functions, initiating new heartbeat with respective values."""
        Service.heartbeatThread = Heartbeat(interval, count, brokerAddress, brokerPort, brokerUsername, brokerPassword, brokerChannel)
        return Service.heartbeatThread.start()

    @staticmethod
    def stopHeartbeat() -> bool:
        """[Docstring] Declares functions, stopping currently running heartbeats."""
        return Service.heartbeatThread.stop()

    @staticmethod
    def monitorHeartbeat() -> float:
        """[Docstring] Declares functions, fetching current heartbeat count."""
        return Service.heartbeatThread.getCount()
