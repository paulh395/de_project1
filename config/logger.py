import logging

# create a logger object
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# create a file handler that logs messages to a file
log_directory = '/'
handler = logging.FileHandler("app.log")
handler.setLevel(logging.DEBUG)

# define the log message format
formatter = logging.Formatter('%(asctime)s  -%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# attach the handler to the logger
logger.addHandler(handler)
