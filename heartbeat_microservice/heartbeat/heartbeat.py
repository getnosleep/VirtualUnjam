"""[Docstring] Declares heartbeat thread."""
from paho.mqtt.client import Client, MQTTv311
from threading import Thread
from time import sleep

class Heartbeat(Thread):
    """[Docstring] Declares thread, publishing heartbeats."""

    def __init__(self, interval: float, count: int, brokerAddress: str, brokerPort: int, brokerUsername: str, brokerPassword: str, brokerChannel: str) -> None:
        """[Docstring] Constructing heartbeat thread."""
        Thread.__init__(self)
        self.__running__: bool = False
        self.__interval__: float = interval
        self.__count__: int = count
        self.__client__: Client
        self.__brokerAddress__: str = brokerAddress
        self.__brokerPort__: int = brokerPort
        self.__brokerUsername__: str = brokerUsername
        self.__brokerPassword__: str = brokerPassword
        self.__brokerChannel__: str = brokerChannel
    
    def run(self) -> None:
        """[Docstring] Function handling lifetime of a heartbeat."""
        try:
            self.__running__ = True
            self.__client__: Client = Client(client_id="heartbeatPublisher",
                                    clean_session=False,
                                    userdata=None,
                                    protocol=MQTTv311,
                                    transport="tcp")
            self.__client__.username_pw_set(self.__brokerUsername__, self.__brokerPassword__)
            self.__client__.connect(self.__brokerAddress__, self.__brokerPort__, 60)
            while self.__running__:
                self.__count__ += 1
                payload: bytes = self.__count__.to_bytes(2, "big")
                self.__client__.publish(self.__brokerChannel__, payload=payload, qos=0, retain=False, properties=None)
                sleep(self.__interval__)
        except Exception:
            self.__running__ = False
            raise Exception("EXPECTATION FAILED")
    
    def start(self) -> None:
        """[Docstring] Function starting heartbeats."""
        self.run()

    def stop(self) -> bool:
        """[Docstring] Function stopping heartbeats."""
        self.__running__ = False
        sleep(0.100)
        return not self.is_alive()

    def getClient(self) -> Client:
        """[Docstring] Function serving thread's client."""
        return self.__client__

    def getCount(self) -> float:
        """[Docstring] Function serving current count."""
        return self.__count__
