from .callbacks import Callbacks
from paho.mqtt.client import Client, MQTTv311
from threading import Thread
from ..properties import *
import time

class Subscriber(Thread):
    def __init__(self):
        # Constructing subscriber thread
        Thread.__init__(self)
        self.__running__: bool = False
        self.__client__: Client
    
    def run(self):
        self.__running__ = True
        try:
            self.__client__ = Client(client_id=ID_BROKER, clean_session=False)
            self.__client__.username_pw_set(USERNAME_BROKER, PASSWORD_BROKER)
            self.__client__.on_message = Callbacks.on_message
            self.__client__.connect(ADDRESS_BROKER, PORT_BROKER)
            self.__client__.subscribe(TOPIC_BROKER)
            self.__client__.loop_start()
        except:
            pass
    
    def stop(self):
        # Function stopping subscription
        self.__running__ = False
        self.__client__.unsubscribe(TOPIC_BROKER)
        self.__client__.disconnect()
        self.__client__.loop_stop()
        time.sleep(0.100)
        # return self.__client__.is_alive()
        return not self.__client__.is_connected() # probably better than is_alive, because subscriber threads ends up in clients loop thread

def startSubscription():
    # 'Dirty starter' for subscription thread
    subscriber = Subscriber()
    subscriber.start()
    return subscriber

subscription = startSubscription()
