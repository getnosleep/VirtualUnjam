class AccelerationException(Exception):
    def __init__(self, message='This is neither acceleration nor deceleration... Go away and program Java, BooN'):
        self.message = message
        super().__init__(self.message)

class NoMemberException(Exception):
    def __init__(self, message='This truck is not a convoy member'):
        self.message = message
        super().__init__(self.message)
