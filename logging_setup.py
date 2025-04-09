import logging

def setup_logger(name,logfile='server1.log',level=logging.DEBUG):
    logger1=logging.getLogger(name)
    logger1.setLevel(level)
    if not logger1.handlers:
        file_handler=logging.FileHandler(logfile)
        formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger1.addHandler(file_handler)
    return logger1