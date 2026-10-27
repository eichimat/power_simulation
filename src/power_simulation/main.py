import copy

from power_simulation.network import Network
from power_simulation.utils.client.simulation.battery import Battery
from power_simulation.utils.client.timeline.timelineclient import TimelineClient
from power_simulation.visualisation import Visualisation

home = Network("Home")

solar = TimelineClient()
solar.load_timeline_from_csv("data/solar.csv")

home.add_client("Solar", solar)

internal = TimelineClient()
internal.load_timeline_from_csv("data/internal.csv", invert=True)
home.add_client("Internal", internal)

#car = Battery(capacity=79, initial_charge=40, max_charge_rate=11, max_discharge_rate=0)
#home.add_client("Internal Power", car)

home_with_battery = copy.deepcopy(home)
home_with_battery.name = "Home + Battery"
battery = Battery(capacity=10.0, initial_charge=6, max_charge_rate=3.5, max_discharge_rate=3.5)

home_with_battery.add_client("Battery", battery)

start_time, end_time = home.get_simulate_period()

home.simulate(start_time=start_time, end_time=end_time)
home_with_battery.simulate(start_time=start_time, end_time=end_time)

v = Visualisation(start_time, end_time)
v.add_timeline(home, 'Grid', 'Power')
v.add_timeline(home, 'Solar', 'Power')
v.add_timeline(home, 'Internal', 'Power')
v.add_timeline(home_with_battery, 'Grid', 'Power')
v.add_timeline(home_with_battery, 'Battery', 'Power')
v.add_timeline(home_with_battery, 'Battery', 'Charge', True)

v.show()

