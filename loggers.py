import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/database.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
database_logger = logging.getLogger(__name__)


logging.basicConfig(
    handlers=[
        logging.FileHandler("logs/handlers.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
handlers_logger = logging.getLogger(__name__)


logging.basicConfig(
    handlers=[
        logging.FileHandler("logs/main.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
main_logger = logging.getLogger(__name__)