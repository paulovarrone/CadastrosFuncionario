import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Criar manipulador para INFO
    info_handler = RotatingFileHandler(os.path.join(log_directory, 'infoLogs.log'))
    info_handler.setLevel(logging.INFO)
    info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    info_handler.setFormatter(info_formatter)

    # Criar manipulador para WARNING
    warning_handler = RotatingFileHandler(os.path.join(log_directory, 'warningLogs.log'))
    warning_handler.setLevel(logging.WARNING)
    warning_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    warning_handler.setFormatter(warning_formatter)

    # Criar manipulador para ERROR
    error_handler = RotatingFileHandler(os.path.join(log_directory, 'errorLogs.log'))
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    error_handler.setFormatter(error_formatter)

    # Configurar o logger principal
    logger = logging.getLogger()
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)

    # Também pode configurar um manipulador de console, se necessário
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
