import numpy as np
import gurobipy as gp
from gurobipy import GRB
import QuantLib as ql

# Financial data for stocks
stocks = ['Stock1', 'Stock2', 'Stock3']
expected_returns = np.array([0.08, 0.1, 0.12])
cov_matrix = np.array([
    [0.04, 0.02, 0.01],
    [0.02, 0.09, 0.03],
    [0.01, 0.03, 0.05]
])

# Bond data
yield_rate = 0.035  # Yield rate for the bond
maturity = 5  # Maturity in years
face_value = 1000  # Face value of the bond


def optimize_portfolio(expected_returns, cov_matrix):
    num_assets = len(expected_returns)
    model = gp.Model("Portfolio Optimization")

    # Create variables for portfolio weights
    weights = model.addVars(num_assets, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="weights")

    # Set objective: minimize portfolio variance
    portfolio_variance = gp.quicksum(weights[i] * cov_matrix[i, j] * weights[j] for i in range(num_assets) for j in range(num_assets))
    model.setObjective(portfolio_variance, GRB.MINIMIZE)

    # Add constraint: sum of weights equals 1 (fully invested)
    model.addConstr(weights.sum() == 1, "budget")

    # Optimize the model
    model.optimize()

    # Return optimal weights
    if model.status == GRB.OPTIMAL:
        optimal_weights = np.array([weights[i].x for i in range(num_assets)])
        return optimal_weights
    else:
        return None


# Example usage of portfolio optimization
optimal_weights = optimize_portfolio(expected_returns, cov_matrix)
if optimal_weights is not None:
    print("Optimal portfolio weights:")
    for i in range(len(stocks)):
        print(f"{stocks[i]}: {optimal_weights[i]:.4f}")


def bond_valuation(yield_rate, maturity, face_value):
    # Set up QuantLib bond object
    today = ql.Date.todaysDate()
    ql.Settings.instance().evaluationDate = today

    # Define bond parameters
    settlement_days = 0
    calendar = ql.UnitedStates(ql.UnitedStates.Settlement)
    day_count = ql.Thirty360(ql.Thirty360.BondBasis)  # Specify the bond basis convention
    coupon_rate = 0.05  # Assuming a fixed coupon rate for simplicity

    # Construct bond schedule
    issue_date = today
    maturity_date = calendar.advance(issue_date, ql.Period(maturity, ql.Years))
    schedule = ql.Schedule(issue_date, maturity_date,
                           ql.Period(ql.Annual), calendar,
                           ql.Unadjusted, ql.Unadjusted,
                           ql.DateGeneration.Backward, False)

    # Create fixed rate bond
    bond = ql.FixedRateBond(settlement_days, face_value, schedule, [coupon_rate], day_count)

    # Set bond pricing engine
    discount_curve = ql.YieldTermStructureHandle(ql.FlatForward(today, ql.QuoteHandle(ql.SimpleQuote(yield_rate)), day_count))
    bond.setPricingEngine(ql.DiscountingBondEngine(discount_curve))

    # Calculate present value (NPV)
    present_value = bond.NPV()

    return present_value


# Example bond valuation
yield_rate = 0.03
maturity = 5
face_value = 1000

bond_value = bond_valuation(yield_rate, maturity, face_value)
print(f"Present value of the bond: ${bond_value:.2f}")
