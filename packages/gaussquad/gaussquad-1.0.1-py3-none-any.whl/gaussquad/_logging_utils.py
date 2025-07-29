from contextlib import contextmanager
import sys
import logging

logger = logging.getLogger(__name__)


@contextmanager
def logging_context(verbose):
    """
    Context manager to temporarily enable debug logging.
    Ensures logger state is reset afterward.
    """
    original_level = logger.level
    if not verbose:
        yield
        return

    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(levelname)s: %(message)s\n")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    try:
        yield
    finally:
        logger.removeHandler(handler)
        logger.setLevel(original_level)
