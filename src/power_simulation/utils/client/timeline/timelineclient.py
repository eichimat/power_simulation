from datetime import datetime, timedelta

from power_simulation.utils.client.powerclient import PowerClient


class TimelineClient(PowerClient):
    def __init__(self):
        super().__init__()
        self.timeline: dict[datetime, float] = {}  # Dictionary mapping timestamps to power flows

    def get_min_time(self) -> datetime:
        if not self.timeline:
            raise ValueError("Timeline is empty. Please load a timeline before querying.")
        return min(self.timeline.keys())

    def get_max_time(self) -> datetime:
        if not self.timeline:
            raise ValueError("Timeline is empty. Please load a timeline before querying.")
        return max(self.timeline.keys())    

    def load_timeline_from_csv(self, file_path: str, invert: bool=False, multiplier: float=0.001) -> None:
        """
        Load a timeline from a CSV file.
        The CSV file should have two columns: timestamp and power flow (in kW).
        The timestamp should be in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).
        """
        import csv

        self.timeline = {}
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            #next(reader)  # Skip header
            for row in reader:
                timestamp = datetime.fromisoformat(row[0])
                power_flow = multiplier * float(row[1].replace(',', '.'))  # Replace comma with dot for decimal
                if invert:
                    power_flow = -power_flow
                self.timeline[timestamp] = power_flow

    def get_power_at_time(self, time: datetime) -> float:
        if not hasattr(self, 'timeline'):
            raise ValueError("Timeline not loaded. Please load a timeline before querying power.")
        # If the time is outside the timeline range, return the last known power value
        if time not in self.timeline:
            raise ValueError("Time is outside the timeline range.")
        
        power = self.timeline[time]
        return power

    def get_power_flow(self, time: datetime, available_power: float, duration: timedelta) -> float:  
        """
        Returns the current power flow in kW.
        Positive values indicate power generation, while negative values indicate power consumption.
        """
        if time is None:
            raise ValueError("Time must be provided to get power flow.")
        return self.get_power_at_time(time)