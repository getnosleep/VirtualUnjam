"""[Docstring] Declares heartbeat thread."""
from ..initializer import initialize
from .callbacks import Callbacks
from paho.mqtt.client import Client, MQTTv311
from threading import Thread
from ..properties import ADDRESS_BROKER, PORT_BROKER, TOPIC_HEARTBEAT, USERNAME_BROKER, PASSWORD_BROKER
import time

__initialized__ = False

class Subscriber(Thread):
    """[Docstring] Declares thread, subscribing to heartbeat broker."""

    def __init__(self, brokerAddress: str, brokerPort: int, brokerUsername: str, brokerPassword: str, brokerChannel: str) -> None:
        """[Docstring] Constructing subscriber thread."""
        Thread.__init__(self, daemon=True)
        self.__running__ = False
        self.__client__: Client
        self.__brokerAddress__ = brokerAddress
        self.__brokerPort__ = brokerPort
        self.__brokerUsername__ = brokerUsername
        self.__brokerPassword__ = brokerPassword
        self.__brokerChannel__ = brokerChannel
    
    def run(self) -> None:
        """[Docstring] Function handling lifetime of a subscriber."""
        self.__running__ = True
        self.__client__ = Client(client_id="heartbeatSubscriber",
                                clean_session=False,
                                userdata=None,
                                protocol=MQTTv311,
                                transport="tcp")
        self.__client__.username_pw_set(self.__brokerUsername__, self.__brokerPassword__)
        self.__client__.on_message = Callbacks.on_message
        self.__client__.connect(self.__brokerAddress__, self.__brokerPort__, 60)
        self.__client__.subscribe(self.__brokerChannel__, 0)
        self.__client__.loop_start()

        while not self.__client__.is_connected() and self.__running__:
            time.sleep(0.025)
    
    def stop(self) -> bool: # does not work correctly yet
        """[Docstring] Function stopping subscription."""
        self.__running__ = False
        self.__client__.unsubscribe(self.__brokerChannel__, 0)
        self.__client__.disconnect()
        self.__client__.loop_stop()
        time.sleep(0.100)
        # return self.__client__.is_alive()
        return not self.__client__.is_connected() # probably better than is_alive, because subscriber threads ends up in clients loop thread

    def getClient(self) -> Client:
        """[Docstring] Function serving thread's client."""
        return self.__client__

    def getConnectionStatus(self) -> bool:
        """[Docstring] Function serving connection status."""
        return self.__client__.is_connected()

    def getCount(self) -> float:
        """[Docstring] Function serving current heatbeat."""
        return Callbacks.heartbeat
    
def __onStart__():
    global __initialized__
    if not __initialized__:
        initialize()
        __initialized__ = True

def startService():
    # Initialization when a truck is startet
    __onStart__()
    subscriber = Subscriber(ADDRESS_BROKER, PORT_BROKER, USERNAME_BROKER, PASSWORD_BROKER, TOPIC_HEARTBEAT)
    subscriber.start()
    return subscriber

subscription = startService()
