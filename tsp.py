import gurobipy as gp
from gurobipy import GRB

# Define the cost matrix for the cities
cost_matrix = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
num_cities = len(cost_matrix)

# Create a new model
model = gp.Model("TSP")

# Create variables
x = {}
for i in range(num_cities):
    for j in range(num_cities):
        if i != j:
            x[i, j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")

# Set objective: minimize total cost
model.modelSense = GRB.MINIMIZE
model.setObjective(gp.quicksum(cost_matrix[i][j] * x[i, j] for i in range(num_cities) for j in range(num_cities) if i != j))

# Add constraints: each city is visited exactly once
for i in range(num_cities):
    model.addConstr(gp.quicksum(x[i, j] for j in range(num_cities) if i != j) == 1, f"Visit_{i}")

for j in range(num_cities):
    model.addConstr(gp.quicksum(x[i, j] for i in range(num_cities) if i != j) == 1, f"Leave_{j}")

# Optimize the model
model.optimize()

# Print the optimal tour and cost
if model.status == GRB.OPTIMAL:
    tour = []
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j and x[i, j].x > 0.5:
                tour.append((i, j))
    print("Optimal tour:")
    for city in tour:
        print(f"City {city[0]} -> City {city[1]}, Cost = {cost_matrix[city[0]][city[1]]}")
    print("Optimal cost:", model.objVal)
else:
    print("No solution found")