"""[Docstring] Declares heartbeat exceptions."""

class HeartbeatConnectionException(Exception):
    """[Docstring] Declares heartbeat connection exceptions."""

    def __init__(self, message: str):
        """[Docstring] Initiates heartbeat connection exceptions."""
        self.message = message
        Exception.__init__(self, self.message)

class HeartbeatPublishException(Exception):
    """[Docstring] Declares heartbeat publish exceptions."""

    def __init__(self, message: str):
        """[Docstring] Initiates heartbeat publish exceptions."""
        self.message = message
        Exception.__init__(self, self.message)