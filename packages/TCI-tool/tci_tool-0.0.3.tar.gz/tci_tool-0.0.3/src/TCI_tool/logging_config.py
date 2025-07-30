import logging
import sys

def configure_logging():
    # Configure the root logger
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Stream handler to stdout
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    # A nice, consistent format
    fmt = logging.Formatter(
        "%(asctime)s %(levelname)-8s [%(name)s:%(lineno)d] %(message)s"
    )
    ch.setFormatter(fmt)

    # Avoid adding multiple handlers if configure_logging
    # gets called more than once:
    if not root.handlers:
        root.addHandler(ch)