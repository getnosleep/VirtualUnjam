"""[Docstring] Declares functions, running the subscription thread."""
from .callbacks import Callbacks
from .subscriber import Subscriber

class Service:
    """[Docstring] Static class, holding and managing the microservice's subscriber thread."""

    subscriber: Subscriber
    flag: bool = False

    @staticmethod
    def subscribe(brokerAddress: str, brokerPort: int, brokerUsername: str, brokerPassword: str, brokerChannel: str) -> bool:
        """[Docstring] Subscribes to heartbeat broker."""
        if not Service.flag:
            Service.flag = True
            Service.subscriber = Subscriber(brokerAddress, brokerPort, brokerUsername, brokerPassword, brokerChannel)
            return Service.subscriber.start()
        else: 
            return Service.subscriber.start()

    @staticmethod
    def unsubscribe() -> bool:
        """[Docstring] Unsubscribes from heartbeat broker."""
        Service.flag = False
        return Service.subscriber.stop()

    @staticmethod
    def monitorHeartbeat() -> float:
        """[Docstring] Monitors heartbeat."""
        return Callbacks.heartbeat