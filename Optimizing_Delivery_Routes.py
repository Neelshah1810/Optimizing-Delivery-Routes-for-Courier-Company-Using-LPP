import streamlit as st
from pulp import *

def courier_optimization(num_vehicles, num_locations, distances, demands, capacities):
    locations = ['W'] + [chr(65 + i) for i in range(num_locations)]
    
    prob = LpProblem("Courier_Delivery", LpMinimize)
    
    # Decision variables for routes
    x = {f'x{v}_{i}{j}': LpVariable(f'x{v}_{i}{j}', cat='Binary') 
         for v in range(num_vehicles) for i in locations for j in locations if i != j}
    
    # Modified: Delivery amount variables (continuous) for each vehicle to each location
    d = {f'd{v}_{j}': LpVariable(f'd{v}_{j}', lowBound=0, upBound=demands[j]) 
         for v in range(num_vehicles) for j in locations[1:]}
    
    # Vehicle visits a location (binary)
    y = {f'y{v}_{j}': LpVariable(f'y{v}_{j}', cat='Binary') 
         for v in range(num_vehicles) for j in locations[1:]}
    
    # Objective function: Minimize total distance
    prob += lpSum(distances[f'{i}{j}'] * x[f'x{v}_{i}{j}'] 
                  for v in range(num_vehicles) 
                  for i in locations 
                  for j in locations if i != j)
    
    # Warehouse Constraints
    for v in range(num_vehicles):
        # Each vehicle must leave warehouse if it's used
        prob += lpSum(x[f'x{v}_W{j}'] for j in locations[1:]) <= 1
        # Each vehicle must return to warehouse if it's used
        prob += lpSum(x[f'x{v}_{i}W'] for i in locations[1:]) <= 1
    
    # Flow conservation constraints
    for v in range(num_vehicles):
        for k in locations[1:]:
            prob += (lpSum(x[f'x{v}_{i}{k}'] for i in locations if i != k) ==
                    lpSum(x[f'x{v}_{k}{j}'] for j in locations if j != k))
    
    # Modified: Location visit constraints
    # Link y variables with x variables - if a vehicle delivers anything, it must visit
    for v in range(num_vehicles):
        for j in locations[1:]:
            # If there's a delivery (d > 0), there must be a visit (y = 1)
            prob += d[f'd{v}_{j}'] <= demands[j] * y[f'y{v}_{j}']
            # If there's a visit (x = 1 for any incoming edge), y must be 1
            prob += lpSum(x[f'x{v}_{i}{j}'] for i in locations if i != j) == y[f'y{v}_{j}']
    
    # Modified: Demand satisfaction constraints
    # Total delivery to each location must equal its demand
    for j in locations[1:]:
        prob += lpSum(d[f'd{v}_{j}'] for v in range(num_vehicles)) == demands[j]
    
    # Capacity constraints for each vehicle
    for v in range(num_vehicles):
        prob += lpSum(d[f'd{v}_{j}'] for j in locations[1:]) <= capacities[v]
    
    # Subtour elimination constraints
    u = {}
    for v in range(num_vehicles):
        for j in locations[1:]:
            u[f'u{v}_{j}'] = LpVariable(f'u{v}_{j}', lowBound=0, upBound=len(locations)-1)
    
    # MTZ subtour elimination
    for v in range(num_vehicles):
        for i in locations[1:]:
            for j in locations[1:]:
                if i != j:
                    prob += u[f'u{v}_{i}'] - u[f'u{v}_{j}'] + len(locations) * x[f'x{v}_{i}{j}'] <= len(locations) - 1
    
    # Solving the problem
    prob.solve()
    
    # Extracting the result
    result = {
        "status": LpStatus[prob.status],
        "routes": {},
        "total_distance": None,
        "deliveries": {},
        "objective_function": prob.objective,
        "constraints": prob.constraints
    }
    
    # Calculating routes, deliveries, and total distance
    if LpStatus[prob.status] == "Optimal":
        routes = {v: [] for v in range(num_vehicles)}
        deliveries = {v: {} for v in range(num_vehicles)}
        
        # Extract deliveries
        for v in range(num_vehicles):
            for j in locations[1:]:
                delivery_amount = d[f'd{v}_{j}'].varValue
                if delivery_amount > 0:
                    deliveries[v][j] = delivery_amount
        
        # Extract routes
        for v in range(num_vehicles):
            current = 'W'
            route = ['W']
            while True:
                next_loc = None
                for j in locations:
                    if j != current and x[f'x{v}_{current}{j}'].varValue > 0.9:
                        next_loc = j
                        break
                if next_loc is None or next_loc == 'W':
                    if len(route) > 1:
                        route.append('W')
                    break
                route.append(next_loc)
                current = next_loc
            if len(route) > 1:
                routes[v] = route
        
        result["routes"] = routes
        result["deliveries"] = deliveries
        result["total_distance"] = value(prob.objective)
    
    return result

# Streamlit App
st.title("Courier Route Optimization with Split Deliveries")

# Input Section
st.header("Input Parameters")
num_vehicles = st.number_input("Number of Vehicles", min_value=1, value=2, step=1)
num_locations = st.number_input("Number of Locations (excluding warehouse)", min_value=1, value=2, step=1)

# Distance inputs
distances = {}
st.subheader("Distances Between Locations")
locations = ['W'] + [chr(65 + i) for i in range(num_locations)]
for i in locations:
    for j in locations:
        if i != j:
            distances[f'{i}{j}'] = st.number_input(f"Distance from {i} to {j}", min_value=0.0, value=10.0)

# Demand inputs
demands = {}
st.subheader("Parcel Demands")
for loc in locations[1:]:
    demands[loc] = st.number_input(f"Demand at {loc}", min_value=0.0, value=5.0)

# Capacity inputs
capacities = {}
st.subheader("Vehicle Capacities")
for v in range(num_vehicles):
    capacities[v] = st.number_input(f"Capacity of Vehicle {v+1}", min_value=0.0, value=15.0)

# Optimization button
if st.button("Optimize"):
    with st.spinner("Solving..."):
        result = courier_optimization(num_vehicles, num_locations, distances, demands, capacities)
    st.success("Optimization Complete!")
    
    # Output Section
    st.subheader("Results")
    
    if result["status"] == "Optimal":
        # Display the objective function
        st.subheader("Objective Function")
        st.code(str(result["objective_function"]))
        
        # Display the constraints
        st.subheader("Constraints")
        with st.expander("Show Constraints"):
            for name, constraint in result["constraints"].items():
                st.code(f"{name}: {constraint}")
        
        # Display total minimum distance
        st.subheader(f"Total Minimum Distance: {result['total_distance']}")
        
        # Display routes and deliveries
        st.subheader("Routes and Deliveries:")
        routes_shown = False
        for v, route in result["routes"].items():
            if len(route) > 1:
                st.write(f"Vehicle {v+1}")
                st.write(f"Route: {' -> '.join(route)}")
                st.write("Deliveries:")
                for loc, amount in result["deliveries"][v].items():
                    st.write(f"Location {loc}: {amount:.2f} units")
                routes_shown = True
        
        if not routes_shown:
            st.info("No vehicles were used in the optimal solution.")
        
        # Display status
        st.subheader(f"Status: {result['status']}")
    else:
        st.error("No feasible solution found!")