from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio

# 1. Keep the native VS Code split-screen tab renderer active
pio.renderers.default = "browser"

# 2. Setup your raw dictionary with datetime objects as keys and floats as values
base_date = datetime(2026, 1, 1)
sample_dict = {
    (base_date + timedelta(days=i)): float(50.0 + np.sin(i / 10) * 15 + np.random.normal(0, 2))
    for i in range(100)
}

# 3. Method A: Convert the dict directly to a Pandas DataFrame (Recommended for labels)
df = pd.DataFrame(list(sample_dict.items()), columns=["Timestamp", "Value"])

# 4. Generate the line plot using the parsed dictionary data
fig = px.line(
    df, 
    x="Timestamp", 
    y="Value", 
    title="Dictionary Data Time-Series (Float over Datetime)",
    labels={"Timestamp": "Calendar Date", "Value": "Float Parameter Metric"}
)

# 5. Visual polishing and filter configurations
fig.update_layout(
    template="plotly_white",
    hovermode="x unified"
)

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector={
        "buttons": [
            {"count": 7, "label": "1w", "step": "day", "stepmode": "backward"},
            {"count": 1, "label": "1m", "step": "month", "stepmode": "backward"},
            {"step": "all", "label": "Reset View"}
        ]
    }
)

if __name__ == "__main__":
    fig.show()
