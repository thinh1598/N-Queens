import time
from ilp_cp_solvers import solve_ortools_cpsat, solve_gurobi, solve_cplex

# Import đúng tên file của bạn (Giả sử là sequential)
from sequential import run_sat_solver 

def solve_sat(N):
    try:
        return run_sat_solver(N)
    except Exception as e:
        return f"Lỗi: {e}"

def main():
    test_sizes = [20, 50, 80, 100] 
    
    print(f"{'N':<5} | {'CP-SAT':<10} | {'Gurobi':<10} | {'CPLEX':<10} | {'SAT (Glucose)':<15}")
    print("-" * 60)
    
    for N in test_sizes:
        t_cpsat = solve_ortools_cpsat(N)
        t_gurobi = solve_gurobi(N)
        t_cplex = solve_cplex(N)
        t_sat = solve_sat(N) 
        
        if isinstance(t_sat, str):
            print(f"LỖI TẠI N={N}: {t_sat}")
        
        def format_t(t):
            if isinstance(t, float): return f"{t:.4f}s"
            return "Limit/Error" if t else "Timeout"
            
        print(f"{N:<5} | {format_t(t_cpsat):<10} | {format_t(t_gurobi):<10} | {format_t(t_cplex):<10} | {format_t(t_sat):<15}")

if __name__ == "__main__":
    main()