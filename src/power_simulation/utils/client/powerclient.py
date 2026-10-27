from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from power_simulation.utils.timeline.timeline import Timeline


class PowerClient(ABC):
    
    def __init__(self):
        self._timelines: dict[str, Timeline] = {}
        self._timelines["Power"] = Timeline()

    @abstractmethod
    def get_power_flow(self, time: datetime | None, available_power: float | None, duration: timedelta) -> float:
        """
        Returns the current power flow in kW.
        Positive values indicate power provision to the network, while negative values indicate power consumption from the network.
        """
        return 0.0

    def evaluate_cycle(self, time: datetime | None, available_power: float | None, duration: timedelta) -> float:
        """
        Evaluate the power flow for a given time and available power.
        """
        power_flow = self.get_power_flow(time, available_power, duration)
        self._timelines["Power"].add_entry(time, power_flow)

        return power_flow

    def register_timeline(self, timeline_name: str) -> Timeline:
        """
        Register a new timeline for the client.
        """
        if timeline_name not in self._timelines:
            self._timelines[timeline_name] = Timeline()
        else:
            raise ValueError(f"Timeline '{timeline_name}' already exists for this client.")

        return self._timelines[timeline_name]
                

    def get_timeline(self, timeline_name: str) -> Timeline:
        """
        Get the timeline for a given name.
        """
        return self._timelines[timeline_name]

    def reset_timelines(self) -> None:
        """
        Reset all timelines for the client.
        """
        for timeline in self._timelines.values():
            timeline.reset()