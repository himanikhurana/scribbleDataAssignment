import logging

logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def LoggingInfo(msg):
    logging.info(msg)


def LoggingError(msg):
    logging.error(msg)
    
