import logging

def main(level):
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logger = logging.basicConfig(level=level, format=('%(filename)s: '    
                                    '%(levelname)s: '
                                    '%(funcName)s(): '
                                    '%(lineno)d:\t'
                                    '%(message)s')
                        )
    return logger
    

