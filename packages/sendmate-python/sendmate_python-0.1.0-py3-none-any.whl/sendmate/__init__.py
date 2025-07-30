from .client import SendMate
from .types import PaymentType, Currency, TransactionStatus
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('SENDMATE')

__version__ = "0.1.0"
__all__ = ["SendMate", "PaymentType", "Currency", "TransactionStatus"] 




