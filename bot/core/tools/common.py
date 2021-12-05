"""
Contain common classes
"""


class MetaSingleton(type):
    """
    Realize pattern Singleton
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PlugCommand:
    """
    Empty discord command implementation with command name only

    Made for the implementation single handlers for discord commands and listeners
    """

    def __init__(self, name: str):
        """
        :param name: command name
        """
        self.name = name
