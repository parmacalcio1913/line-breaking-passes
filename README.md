# Line-Breaking Passes Detection

A Python implementation for detecting line-breaking passes in football using tracking data, developed by Parma Calcio 1913's Data&Analytics team.

## Overview

This project analyzes tracking data to identify when passes break through defensive lines by clustering players and detecting ball trajectory intersections with defensive formations. The implementation is inspired by Stats Perform's work and provides metrics for tactical analysis.

## Installation
Make sure you use Python 3.8.x.
### Clone repo and install requirements
```bash
git clone https://github.com/parmacalcio1913/line-breaking-passes.git
cd line-breaking-passes
python3 -m venv venv
source venv/bin/activate
pip install -r requirements
```

### Download sample data
Data is taken from: [Metrica Sports](https://github.com/metrica-sports/sample-data)
```bash
mkdir Sample_Game_1
cd Sample_Game_1
wget https://raw.githubusercontent.com/metrica-sports/sample-data/master/data/Sample_Game_1/Sample_Game_1_RawEventsData.csv
wget https://raw.githubusercontent.com/metrica-sports/sample-data/master/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Away_Team.csv
wget https://raw.githubusercontent.com/metrica-sports/sample-data/master/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Home_Team.csv
```
In the repo you can already find `Metrica_IO.py`, which contains all the loading utilities taken from [Laurie Shaw's library](https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking)

## Usage
Run the `linebreaking_passes.ipynb`

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

## Features

- **Line Detection**: Automatically identifies three defensive lines (attack, midfield, defense) using hierarchical clustering
- **Pass Classification**: Determines whether passes break lines "through" or "around" defensive formations
- **Metrics Calculation**: Computes number of lines broken and identifies the last line broken
- **Forward Pass Analysis**: Focuses on progressive passes that advance play toward the goal

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
