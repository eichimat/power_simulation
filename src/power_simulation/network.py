from datetime import datetime, timedelta

from power_simulation.utils.client.grid import Grid
from power_simulation.utils.client.powerclient import PowerClient
from power_simulation.utils.client.simulation.simulationclient import SimulationClient
from power_simulation.utils.client.timeline.timelineclient import TimelineClient


class Network:
    def __init__(self, network_name: str, time_resulution: timedelta = timedelta(minutes=5)):

        self._name = network_name
        self._power_clients: dict[str, PowerClient] = {} # contains all clients
        
        self._power_clients['Grid'] = Grid()  # Initialize the grid as a PowerClient
        self._time_resolution = time_resulution  # Time resolution in sec

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, network_name: str):
        self._name = network_name

    def add_client(self, client_name: str, client: PowerClient) -> None:
        self._power_clients[client_name] = client

    def get_client(self, client_name: str) -> PowerClient:
        return self._power_clients[client_name]
    
    def get_simulate_period(self):
        """
        Get the simulation period based on the timeline clients.
        Returns a tuple of (start_time, end_time).
        """


        start_times = [client.get_min_time() for client in self._power_clients.values() if isinstance(client, TimelineClient)]
        end_times = [client.get_max_time() for client in self._power_clients.values() if isinstance(client, TimelineClient)]

        if len(start_times)<=0:
            raise ValueError("No timeline clients defined.")

        return max(start_times), min(end_times)

    def evaluate_network(self, time: datetime) -> None:
        """
        Evaluate the power flow for all clients in the network.
        Returns the total power flow in kW.
        """
        total_power = 0.0
        
        for client in self._power_clients.values():
            if isinstance(client, TimelineClient):
                total_power += client.evaluate_cycle(time, None, self._time_resolution)  # Timeline clients don't need available power

        for client in self._power_clients.values():
            if isinstance(client, SimulationClient):
                total_power += client.evaluate_cycle(time, total_power, self._time_resolution)  # Simulated clients need available power

        self.get_client('Grid').evaluate_cycle(time, total_power, self._time_resolution)  # Evaluate the grid as well

    def simulate(self, start_time: datetime, end_time: datetime) -> None:
        """
        Simulate the network from start_time to end_time.
        """
        current_time = start_time
        while current_time <= end_time:
            self.evaluate_network(current_time)
            current_time += self._time_resolution