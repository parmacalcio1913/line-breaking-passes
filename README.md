# Line-Breaking Passes Detection

A Python implementation for detecting line-breaking passes in football using tracking data, developed by Parma Calcio 1913's Data&Analytics team.

## Overview

This project analyzes tracking data to identify when passes break through defensive lines by clustering players and detecting ball trajectory intersections with defensive formations. The implementation is inspired by Stats Perform's work and provides metrics for tactical analysis.

## Features

- **Line Detection**: Automatically identifies three defensive lines (attack, midfield, defense) using hierarchical clustering
- **Pass Classification**: Determines whether passes break lines "through" or "around" defensive formations  
- **Metrics Calculation**: Computes number of lines broken and identifies the last line broken
- **Forward Pass Analysis**: Focuses on progressive passes that advance play toward the goal

## Method

### Line Detection
- Players are clustered along the x-axis using **Ward's hierarchical clustering** method
- Goalkeepers are excluded from clustering
- Three clusters represent attack, midfield, and defense lines
- Lines are defined as connections between adjacent players in the same cluster plus sidelines

### Pass Analysis
- Ball trajectory is modeled as a straight line between pass start and end coordinates
- Defensive lines are "frozen" at pass start and end frames
- Passes breaking lines must intersect the same line at both start and end of the pass
- Additional constraints ensure realistic line-breaking detection

### Constraints
- **Distance Requirements**: Ball must be ≥1m from broken line at pass start and end
- **Segment Limits**: Broken segments must be ≤9m (x-axis) and ≤20m (y-axis)
- **Forward Movement**: Only analyzes passes that advance toward the goal

## Installation

### Prerequisites
```bash
pip install torch numpy scipy
```

### Required Files
- `Metrica_IO.py` - Data loading utilities from [Laurie Shaw's library](https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking)
- `helper.py` - Contains the `intersects` function for line intersection detection
- Sample data from [Metrica Sports](https://github.com/metrica-sports/sample-data)

## Usage

### Basic Implementation
```python
import torch
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from Metrica_IO import tracking_data, to_metric_coordinates, read_event_data
from helper import intersects

# Configuration
DEVICE = "cpu"
DTYPE = torch.float32
XDIM, YDIM = 105, 68
DATADIR = "."
GAMEID = 1
PERIOD = 1

# Load and process data
tracking_home = tracking_data(DATADIR=DATADIR, game_id=GAMEID, teamname="Home")
tracking_away = tracking_data(DATADIR=DATADIR, game_id=GAMEID, teamname="Away")
events_df = read_event_data(DATADIR, GAMEID)

# Convert to metric coordinates
events_df = to_metric_coordinates(events_df)
tracking_home = to_metric_coordinates(tracking_home)
tracking_away = to_metric_coordinates(tracking_away)

# Filter for specific period
tracking_home = tracking_home.query("Period==1")
tracking_away = tracking_away.query("Period==1")
```

### Configuration Parameters
```python
# Distance constraints
MAX_DISTANCE_DEFENDERS_X = 9    # Maximum segment width (x-axis)
MAX_DISTANCE_DEFENDERS_Y = 20   # Maximum segment width (y-axis)
MIN_DISTANCE_BEFORE_LINE = 1    # Minimum distance from line at pass start
MIN_DISTANCE_AFTER_LINE = 1     # Minimum distance from line at pass end

# Clustering parameters
NB_CLUSTERS = 3                 # Number of defensive lines to detect

# Team direction settings
team_attacking_left_to_right = {
    "Home": True,
    "Away": False
}
```

## Output Metrics

The analysis enhances event data with the following metrics:

- **`last_line_broken`**: The deepest line broken ("attack", "midfield", "defense", or None)
- **`nb_lines_broken`**: Total number of lines broken by the pass
- **`last_line_broken_through_or_around`**: Whether the ball progressed "through" or "around" the line

## Data Structure

### Input Requirements
- **Tracking Data**: Frame-by-frame player positions (x, y coordinates)
- **Event Data**: Pass events with start/end coordinates and timestamps
- **Team Information**: Direction of play and player identification

### Expected Data Format
```python
# Tracking data columns
"Home_1_x", "Home_1_y", "Home_2_x", "Home_2_y", ...
"Away_1_x", "Away_1_y", "Away_2_x", "Away_2_y", ...
"ball_x", "ball_y"

# Event data columns
"Type", "Team", "Period", "Start Frame", "End Frame"
"Start X", "Start Y", "End X", "End Y"
```

## Technical Details

### Coordinate System
- Field dimensions: 105m × 68m
- Coordinates adjusted to center origin: `+XDIM/2`, `+YDIM/2`
- Tracking data converted from normalized to metric coordinates

### Clustering Algorithm
- **Method**: Ward's hierarchical clustering
- **Criterion**: Maximum 3 clusters
- **Sorting**: Clusters ordered by mean x-position
- **Special Cases**: Handles scenarios with fewer than 3 natural clusters

### Performance Considerations
- Uses PyTorch tensors for efficient computation
- Vectorized operations for line intersection detection

## Blog & Resources

For more football analytics tutorials, insights, and open data projects, visit our blog:
**[G.O.A.L. - Gialloblù Open Analytics Lab](https://www.notion.so/Giallobl-Open-Analytics-Lab-4b5f473392624f05a87229ffc16c4b22)**


## References

- [Stats Perform Opta Vision](https://www.statsperform.com/opta-vision/)
- [Metrica Sports Sample Data](https://github.com/metrica-sports/sample-data)
- [Friends of Tracking Data](https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking)


## Support

For questions or discussions about the implementation, reach out on [LinkedIn](https://www.linkedin.com/in/daniel-montalbano-a4839a171/).

## License

This project uses open data and is intended for educational and research purposes.

---

*Developed by the Data&Analytics Team at Parma Calcio 1913*

