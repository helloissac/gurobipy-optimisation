import gurobipy as gp
from gurobipy import GRB
import numpy as np

# Define the expected returns and covariance matrix for the assets
expected_returns = np.array([0.1, 0.2, 0.15])
cov_matrix = np.array([
    [0.005, -0.010, 0.004],
    [-0.010, 0.040, -0.002],
    [0.004, -0.002, 0.023]
])

# Define the number of assets
num_assets = len(expected_returns)

# Create a new model
model = gp.Model("Portfolio Optimization")

# Create variables for portfolio weights
weights = model.addVars(num_assets, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="weights")

# Set objective: minimize portfolio variance (quadratic form)
portfolio_variance = gp.quicksum(
    weights[i] * cov_matrix[i, j] * weights[j] for i in range(num_assets) for j in range(num_assets))
model.setObjective(portfolio_variance, GRB.MINIMIZE)

# Add constraint: sum of weights equals 1 (fully invested)
model.addConstr(weights.sum() == 1, "budget")

# Optimize the model
model.optimize()

# Print the optimal portfolio weights and minimum variance
if model.status == GRB.OPTIMAL:
    optimal_weights = np.array([weights[i].x for i in range(num_assets)])
    optimal_variance = model.objVal  # Get the objective value directly from the model

    print("Optimal portfolio weights:")
    for i in range(num_assets):
        print(f"Asset {i + 1}: {optimal_weights[i]}")

    print("\nMinimum portfolio variance:", optimal_variance)
else:
    print("No solution found")