# Courier Route Optimization using Linear Programming

This project implements a vehicle routing optimization system that handles multiple vehicles, multiple trips, and split deliveries using Linear Programming. It's designed to find the most efficient routes for delivering packages while considering vehicle capacities and delivery demands.

## Features

- Multiple vehicle support
- Split delivery capability (one location can be served by multiple vehicles)
- Multiple trips per vehicle
- Capacity constraints handling
- Distance optimization
- Interactive web interface using Streamlit
- Real-time solution visualization

## Prerequisites

- Python 3.7 or higher
- PuLP (Linear Programming toolkit)
- Streamlit (Web interface)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/courier-optimization.git
cd courier-optimization
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run Optimizing_Delivery_Routes.py
```

2. Input your parameters in the web interface:
   - Number of vehicles
   - Number of locations
   - Maximum trips per vehicle
   - Distances between locations
   - Demands at each location
   - Vehicle capacities

3. Click "Optimize" to get the solution

## Example Scenarios

### Basic Example
```python
num_vehicles = 2
num_locations = 2
distances = {
    'WA': 10, 'WB': 15,
    'AW': 10, 'AB': 8,
    'BW': 15, 'BA': 8
}
demands = {
    'A': 7,
    'B': 3
}
capacities = {
    0: 4,
    1: 4
}
```

### Complex Example
```python
num_vehicles = 3
num_locations = 3
distances = {
    'WA': 5, 'WB': 5, 'WC': 5,
    'AW': 5, 'AB': 10, 'AC': 15,
    'BW': 5, 'BA': 10, 'BC': 10,
    'CW': 5, 'CA': 15, 'CB': 10
}
demands = {
    'A': 10,
    'B': 1,
    'C': 1
}
capacities = {
    0: 4,
    1: 4,
    2: 4
}
```

## Mathematical Model

The optimization model uses:
- Binary variables for route selection
- Continuous variables for delivery amounts
- Constraints for:
  - Flow conservation
  - Demand satisfaction
  - Capacity limits
  - Subtour elimination

## Solution Output

The program outputs:
1. Optimal routes for each vehicle
2. Delivery amounts at each location
3. Total distance traveled
4. Solution status


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Acknowledgments

- Streamlit for the web interface framework
- PuLP for the Linear Programming solver
- Any other acknowledgments you'd like to add

