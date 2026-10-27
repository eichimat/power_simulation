from datetime import datetime

import pandas as pd


class Timeline:
    def __init__(self):
        self._tl: pd.Series = pd.Series(dtype=float, index=pd.DatetimeIndex([], dtype='datetime64[ns]'))

    def add_entry(self, time: datetime, value: float):
        self._tl.loc[time] = value

    def get_timeline(self) -> pd.Series:
        return self._tl
    
    def get_value_range(self, start_time: datetime, end_time: datetime | None = None) -> pd.Series:
        """
        Get the timeline values within a specific time range.
        """

        if end_time is None:
            end_time = start_time
            
        return self._tl.loc[start_time:end_time]

    def reset(self) -> None:
        """
        Reset the timeline by clearing all entries.
        """
        print(self._tl.index)
        self._tl = self._tl.drop(self._tl.index)

    @property
    def name(self):
        return self._name


if __name__ == "__main__":
    # Example usage
    timeline = Timeline()
    timeline.add_entry(datetime(2026, 1, 1, 12, 0), 10.5)
    timeline.add_entry(datetime(2026, 1, 1, 13, 0), 12.3)
    timeline.add_entry(datetime(2026, 1, 1, 14, 0), 9.8)

    print("Full Timeline:", timeline.get_timeline())
    print("Value Range (12:30 to 13:30):", timeline.get_value_range(datetime(2026, 1, 1, 12, 30), datetime(2026, 1, 1, 13, 30)))

    timeline.reset()
    print("Timeline after reset:", timeline.get_timeline())