import sys
from book_recommender.exception.exception_handler import AppException
from book_recommender.logger import log

try:
    a = 6*'5'
    log.info("We are inside try block")
except Exception as e:
    raise AppException(e, sys) from e