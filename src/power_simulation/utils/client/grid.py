
from datetime import datetime

from power_simulation.utils.client.powerclient import PowerClient


class Grid(PowerClient):

    def get_power_flow(self, time: datetime, available_power: float, duration: float) -> float:
        """
        Returns the current power flow in kW.
        Positive values indicate power generation, while negative values indicate power consumption.
        """
        super().get_power_flow(time, available_power, duration)  # Call the parent method to log the power flow
        return -available_power  # The grid can provide or absorb any amount of power