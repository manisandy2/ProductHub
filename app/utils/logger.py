import logging
from app.config.settings import LOG_DIR

LOG_FILE = LOG_DIR / "application.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)