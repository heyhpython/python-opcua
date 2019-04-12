# coding=utf-8
import logging

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%H:%M:%S',
                    )
logging.getLogger('parso.python.diff').disabled = True
logging.getLogger('parso.cache').disabled = True