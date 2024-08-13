from datetime import datetime
class Utils:

    @staticmethod
    def cal_time_elapsed_seconds(start: datetime, end: datetime) -> float:
        return (end - start).total_seconds()