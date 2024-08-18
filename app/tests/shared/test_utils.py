import unittest
from datetime import datetime
from shared.utils import Utils

class TestUtils(unittest.TestCase):

    def test_cal_time_elapsed_seconds(self):
        # Given
        start_time = datetime(2023, 1, 1, 0, 0, 0)
        end_time = datetime(2023, 1, 1, 0, 1, 0)

        # When
        elapsed_seconds = Utils.cal_time_elapsed_seconds(start_time, end_time)

        # Then
        self.assertEqual(elapsed_seconds, 60.0)