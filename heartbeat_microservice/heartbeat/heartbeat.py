"""[Docstring] Declares heartbeat thread."""
from .publisher import Publisher
from .exceptions import HeartbeatConnectionException, HeartbeatPublishException
from threading import Thread
import time

class Heartbeat(Thread):
    """[Docstring] Declares thread, publishing heartbeats."""

    def __init__(self, interval: float, count: int, publisher: Publisher):
        """[Docstring] Constructing heartbeat thread."""
        Thread.__init__(self)
        self.__interval__ = interval # desired value is 0.020 seconds
        self.__count__ = count
        self.__running__ = False
        self.__publisher__ = publisher
    
    def __run__(self):
        """[Docstring] Function handling lifetime of a heartbeat."""
        try:
            self.__running__ = True
            if self.__publisher__.establishConnectionToBroker():
                raise HeartbeatConnectionException("Can Not Connect to Broker")
            while self.__running__:
                self.__count__ += 1
                if not self.__publisher__.publishHearbeatToChannel(self.__count__):
                    raise HeartbeatPublishException("Can Not Publish Message")
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
        self.__publisher__.suspendConnectionToBroker()
        self.__running__ = False
        time.sleep(0.100)
        return not self.is_alive()

    def getCount(self):
        """[Docstring] Function serving current count."""
        return self.__count__
