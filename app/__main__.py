import uvicorn

from app.api import app
from app.core import logger
from app.core.config import Config

config = Config.get()
logger.setup_logging(config.logging)

if __name__ == "__main__":
    uvicorn.run(app, host=config.bot.HOST.compressed, port=config.bot.PORT)
