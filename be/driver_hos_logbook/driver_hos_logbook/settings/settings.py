from .envs.base import Base

class Dev(Base):
    """
    Development settings.
    """
    pass


class Prod(Base):
    """
    Production settings.
    """
    DEBUG = False