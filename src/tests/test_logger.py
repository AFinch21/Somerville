import unittest
import logging
from io import StringIO
from logger.Logger import get_logger, LLM_LOG_LEVEL, COLORS  # Replace `your_module` with your module name.

class TestColoredLogger(unittest.TestCase):
    def setUp(self):
        # Redirect output for testing
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        self.logger = get_logger("test_logger")
        self.logger.handlers.clear()  # Clear existing handlers
        self.logger.addHandler(self.handler)

    def tearDown(self):
        # Cleanup handlers
        self.logger.handlers.clear()

