import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from plotly.subplots import make_subplots

from power_simulation.network import Network


class Visualisation():

    def __init__(self, start: datetime, end: datetime):
        self._df = pd.DataFrame()
        self._start = start
        self._end = end
        self._fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    def add_timeline(self, network: Network, client_name: str, timeline_name: str, secondary_y: bool = False):

        series_name = f"{network.name}: {client_name} {timeline_name}"
        
        self._df[series_name] = network.get_client(client_name).get_timeline(timeline_name).get_value_range(self._start, self._end)
        
        self._fig.add_trace(
            go.Scatter(x=self._df.index, y=self._df[series_name], name=series_name),
            secondary_y=secondary_y
        )

    def show(self):
        self._fig.update_layout(
            title_text="Multi-Series Time Series with Plotly Dual Y-Axes",
            xaxis_title="Timeline Tracker",
            hovermode="x unified", # Shows all series values under a single hover line
            template="plotly_white"
        )

        self._fig.update_yaxes(title_text="Grid Power", secondary_y=False)
        self._fig.update_yaxes(title_text="Charge", secondary_y=True)


        self._fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector={
                "buttons": [
                    {"count": 1, "label": "1d", "step": "day", "stepmode": "backward"},
                    {"count": 7, "label": "1w", "step": "day", "stepmode": "backward"},
                    {"count": 1, "label": "1m", "step": "month", "stepmode": "backward"},
                    {"step": "all", "label": "Reset View"}
                ]
            }
        )

        # 6. Render diagram in the browser window
        self._fig.show()