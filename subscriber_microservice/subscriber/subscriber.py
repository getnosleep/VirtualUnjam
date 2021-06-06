"""[Docstring] Declares heartbeat thread."""
from .callbacks import Callbacks
from paho.mqtt.client import Client, MQTTMessage, MQTTv311
from .exceptions import SubscribeException, SubscriberConnectionException
from threading import Thread
import time

class Subscriber(Thread):
    """[Docstring] Declares thread, subscribing to heartbeat broker."""

    def __init__(self, brokerAddress: str, brokerPort: int, brokerUsername: str, brokerPassword: str, brokerChannel: str) -> None:
        """[Docstring] Constructing subscriber thread."""
        Thread.__init__(self)
        self.__running__ = False
        self.__client__: Client
        self.__brokerAddress__ = brokerAddress
        self.__brokerPort__ = brokerPort
        self.__brokerUsername__ = brokerUsername
        self.__brokerPassword__ = brokerPassword
        self.__brokerChannel__ = brokerChannel
    
    def __run__(self) -> None:
        """[Docstring] Function handling lifetime of a subscriber."""
        try:
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
            self.__client__.loop_start()      # maybe needs to be called in view
        except:
            raise Exception("EXPECTATION FAILED")
    
    def start(self) -> bool:
        """[Docstring] Function starting subscription."""
        if not self.__running__:
            self.__run__()
            # return self.__client__.is_alive()
            return self.__client__.is_connected() # same 406 result but running as is_alive on restart
        else:
            return False
    
    def stop(self) -> bool:
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

    def getCount(self) -> float:
        """[Docstring] Function serving current heatbeat."""
        return Callbacks.heartbeat
