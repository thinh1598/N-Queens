import time
from ortools.sat.python import cp_model
import gurobipy as gp
from gurobipy import GRB
from docplex.mp.model import Model

def solve_ortools_cpsat(N):
    model = cp_model.CpModel()
    queens = [model.NewIntVar(0, N - 1, f'q_{i}') for i in range(N)]
    
    model.AddAllDifferent(queens)
    model.AddAllDifferent([queens[i] + i for i in range(N)])
    model.AddAllDifferent([queens[i] - i for i in range(N)])
    
    solver = cp_model.CpSolver()
    start_time = time.time()
    status = solver.Solve(model)
    return time.time() - start_time if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE else None

def solve_gurobi(N):
    try:
        env = gp.Env(empty=True)
        env.setParam('OutputFlag', 0)
        env.start()
        m = gp.Model("nqueens", env=env)
        
        x = m.addVars(N, N, vtype=GRB.BINARY, name="x")
        m.addConstrs((x.sum(i, '*') == 1 for i in range(N)), name="row")
        m.addConstrs((x.sum('*', j) == 1 for j in range(N)), name="col")
        m.addConstrs((gp.quicksum(x[i, j] for i in range(N) for j in range(N) if i + j == k) <= 1 for k in range(2 * N - 1)), name="diag1")
        m.addConstrs((gp.quicksum(x[i, j] for i in range(N) for j in range(N) if i - j == k) <= 1 for k in range(-N + 1, N)), name="diag2")
        
        start_time = time.time()
        m.optimize()
        return time.time() - start_time if m.SolCount > 0 else None
    except Exception as e:
        return f"Error/License limit: {e}"

def solve_cplex(N):
    try:
        mdl = Model(name='nqueens')
        mdl.parameters.mip.display.set(0)
        x = mdl.binary_var_matrix(N, N, name='x')
        
        mdl.add_constraints(mdl.sum(x[i, j] for j in range(N)) == 1 for i in range(N))
        mdl.add_constraints(mdl.sum(x[i, j] for i in range(N)) == 1 for j in range(N))
        
        for k in range(2 * N - 1):
            mdl.add_constraint(mdl.sum(x[i, j] for i in range(N) for j in range(N) if i + j == k) <= 1)
        for k in range(-N + 1, N):
            mdl.add_constraint(mdl.sum(x[i, j] for i in range(N) for j in range(N) if i - j == k) <= 1)
            
        start_time = time.time()
        sol = mdl.solve()
        return time.time() - start_time if sol else None
    except Exception as e:
        return f"Error/License limit: {e}"