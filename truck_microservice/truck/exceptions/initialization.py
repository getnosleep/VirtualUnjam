class TruckNotInitializedException(Exception):
    """Raised, when a truck is requested, but not yet initialized"""
    def __init__(self, message='The Truck has not been initialized. A request for truck specific parameters is not possible.'):
        self.message = message
        super().__init__(self.message)
