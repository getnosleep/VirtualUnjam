"""[Docstring] Declares heartbeat thread."""
from paho.mqtt.client import Client, MQTTMessage, MQTTv311
from .exceptions import HeartbeatConnectionException, HeartbeatPublishException
from threading import Thread
import time

class Heartbeat(Thread):
    """[Docstring] Declares thread, publishing heartbeats."""

    def __init__(self, interval: float, count: int, brokerAddress: str, brokerPort: int, brokerUsername: str, brokerPassword: str, brokerChannel: str):
        """[Docstring] Constructing heartbeat thread."""
        Thread.__init__(self)
        self.__running__ = False
        self.__interval__ = interval # desired value is 0.020 seconds
        self.__count__ = count
        self.__client__: Client
        self.__brokerAddress__ = brokerAddress
        self.__brokerPort__ = brokerPort
        self.__brokerUsername__ = brokerUsername
        self.__brokerPassword__ = brokerPassword
        self.__brokerChannel__ = brokerChannel
    
    def __run__(self):
        """[Docstring] Function handling lifetime of a heartbeat."""
        try:
            self.__running__ = True
            self.__client__ = Client(client_id="heartbeatPublisher",
                                    clean_session=False,
                                    userdata=None,
                                    protocol=MQTTv311,
                                    transport="tcp")
            self.__client__.username_pw_set(self.__brokerUsername__, self.__brokerPassword__)
            #self.__client__.on_publish = Heartbeat.on_publish
            self.__client__.connect(self.__brokerAddress__, self.__brokerPort__, 60)
            while self.__running__:
                self.__count__ += 1
                payload: bytes = self.__count__.to_bytes(2, "big")
                #print(self.__count__)
                #print(payload)
                self.__client__.publish(self.__brokerChannel__, payload=payload, qos=0, retain=False, properties=None)
                time.sleep(self.__interval__)
        except HeartbeatConnectionException:
            self.__running__ = False
            raise HeartbeatConnectionException("Can Not Connect to Broker")
        except HeartbeatPublishException:
            self.__running__ = False
            raise HeartbeatPublishException("Can Not Publish Message")
        except Exception:
            self.__running__ = False
            raise Exception("EXPECTATION FAILED")
    
    def start(self):
        """[Docstring] Function starting heartbeats."""
        self.__run__()
        return self.is_alive()

    def stop(self):
        """[Docstring] Function stopping heartbeats."""
        self.__running__ = False
        time.sleep(0.100)
        return not self.is_alive()

    def getCount(self):
        """[Docstring] Function serving thread's client."""
        return self.__client__

    def getCount(self):
        """[Docstring] Function serving current count."""
        return self.__count__

    #@staticmethod
    #def on_publish(client: Client, msg: MQTTMessage, interval: float):
    #    """[Docstring] Declares functions, handling message callback."""
    #    time.sleep(interval)
