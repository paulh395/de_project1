import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime

# folder to store log files
BASE_LOG_DIR  = Path(__file__).resolve().parent.parent.parent.parent / "logs"
LOG_DIR = datetime.now().strftime("%Y_%m_%d")
LOG_DIR = BASE_LOG_DIR / LOG_DIR
# create log directory if not exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE  = LOG_DIR / f"{timestamp}__app.log"

def get_logger(
        name:str
    ) -> logging.Logger:
    """
    Function to get a logger instance
    
    Args:
        name (str): Name of the logger

    Returns:
        logging.Logger: Configured logger instance
    
    """
    logger  = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # rotating filer handler
    file_handler = RotatingFileHandler(LOG_FILE, mode ='a', maxBytes=5*1024*1024, backupCount=3,)
    file_handler.setFormatter(formatter)

    # consolde handler 
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

