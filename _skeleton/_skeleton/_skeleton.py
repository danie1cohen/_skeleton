"""
_skeleton
"""

import logging
import logging.config

# from custom_handlers import BufferingSMTPHandler


class Object(object):
    """
    Class docstring
    """
    def __init__(self, logger=None):
        """
        Initializes this object.
        """

        if not logger:
            self.setup_logging()
        else:
            self.logger = logger
            self.logger.debug('Passed in external logger.')

    def setup_logging(self):
        """
        Sets up logging if no logger is passed to the object.
        """
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        handler = logging.FileHandler('default.log')
        handler.setLevel(logging.DEBUG)

        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(format_string)
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.debug('Setup internal logging.')

    def do_something(self):
        """
        describe what it does
        """
        pass
