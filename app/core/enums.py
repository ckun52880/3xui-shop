from enum import Enum

from aiogram.types import BotCommand


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class SubscriptionStatus(str, Enum):
    pass


class PaymentMethod(str, Enum):
    pass


class Command(Enum):
    START = BotCommand(command="start", description="Restart bot")
    HELP = BotCommand(command="help", description="Show help")


class LogLevel(str, Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ArchiveFormat(str, Enum):
    ZIP = "zip"
    GZ = "gz"
