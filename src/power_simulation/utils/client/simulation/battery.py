from datetime import datetime, timedelta

from power_simulation.utils.client.simulation.simulationclient import SimulationClient


class Battery(SimulationClient):
     
    def __init__(self, capacity: float, initial_charge: float = 0.0, max_charge_rate: float = 0.5, max_discharge_rate: float = 0.5):
        
        super().__init__()
        self.capacity = capacity  # in kWh
        self.charge = initial_charge  # in kWh
        self.max_charge_rate = max_charge_rate  # Max charge rate in kW
        self.max_discharge_rate = max_discharge_rate  # Max discharge rate in kW

        self.charge_timeline = self.register_timeline("Charge")  # Timeline for battery charge level

    def charge_battery(self, available_power: float, duration: timedelta) -> float:
        """
        Charge the battery with the available power.
        Returns the power used to charge the battery.
        """

        used_power = min(available_power, self.max_charge_rate)
        usable_energy = used_power * (duration.total_seconds() / 3600)  # Convert kW to kWh

        charged_energy = min(usable_energy, self.capacity - self.charge)
        self.charge += charged_energy

        return charged_energy / (duration.total_seconds() / 3600)  # Return power in kW

    def discharge_battery(self, required_power: float, duration: timedelta) -> float:
        """
        Discharge the battery to provide power.
        Returns the power provided by the battery.
        """

        provided_power = min(required_power, self.max_discharge_rate)
        usable_energy = provided_power * (duration.total_seconds() / 3600)  # Convert kW to kWh

        discharged_energy = min(usable_energy, self.charge)
        self.charge -= discharged_energy

        return discharged_energy / (duration.total_seconds() / 3600)  # Return power in kW

    def get_power_flow(self, time: datetime, available_power: float, duration: timedelta) -> float:
        """
        Returns the current power flow in kW.
        Positive values indicate power provision, while negative values indicate power consumption.
        """
        if available_power is None:
            raise ValueError("Available power must be provided to get power flow.")
        
        if available_power > 0:
            # Charge the battery
            power = -self.charge_battery(available_power, duration)
        else:
            # Discharge the battery
            power = self.discharge_battery(-available_power, duration)

        return power

    def evaluate_cycle(self, time: datetime, available_power: float, duration: timedelta) -> float:
        """
        Evaluate the power flow for a given time and available power.
        """
        super().evaluate_cycle(time, available_power, duration)  # Log the power flow in the base class timeline
        
        power_flow = self.get_power_flow(time, available_power, duration)
        self.charge_timeline.add_entry(time, self.charge)  # Log the current charge level
        
        return power_flow