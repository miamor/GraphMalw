import logging
def log(filename, msg, log_type='info'):
    logging.basicConfig(level=logging.DEBUG, filename=filename, filemode='a+',
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    if log_type == 'info':
        logging.info(msg)
    elif log_type == 'warning':
        logging.warning(msg)
    elif log_type == 'error':
        logging.error(msg)

    print(msg)