import gurobipy as gp
from gurobipy import GRB

# Define the weights and values of the items
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 5

num_items = len(weights)

# Create a new model
model = gp.Model("Knapsack")

# Create variables (binary: 0 or 1)
x = model.addVars(num_items, vtype=GRB.BINARY, name="x")

# Set the objective function (maximize total value)
model.setObjective(gp.quicksum(values[i] * x[i] for i in range(num_items)), GRB.MAXIMIZE)

# Add the capacity constraint
model.addConstr(gp.quicksum(weights[i] * x[i] for i in range(num_items)) <= capacity, "Capacity")

# Optimize the model
model.optimize()

# Retrieve and print the optimal solution
if model.status == GRB.OPTIMAL:
    selected_items = [i for i in range(num_items) if x[i].X > 0.5]
    total_value = sum(values[i] for i in selected_items)
    total_weight = sum(weights[i] for i in selected_items)
    print("Selected items:", selected_items)
    print("Total value:", total_value)
    print("Total weight:", total_weight)
else:
    print("No optimal solution found.")
