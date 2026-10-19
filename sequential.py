import time
from pysat.solvers import Glucose3

new_variables_count = 0

def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]

# ĐÃ SỬA: Truyền thêm 'n' vào hàm để tính toán start không bị lỗi NameError
def generate_new_variables(n, new_variables_count, length):
    start = n ** 2 + new_variables_count
    return [i for i in range(start + 1, start + length)]

# ĐÃ SỬA: Truyền thêm 'n' để đẩy xuống hàm generate_new_variables
def at_most_one(n, clauses, variables):
    global new_variables_count
    # Tối ưu: Nếu mảng chỉ có 1 biến (ví dụ đường chéo góc) thì không cần điều kiện AMO
    if len(variables) <= 1:
        return 
        
    new_variables = generate_new_variables(n, new_variables_count, len(variables))
    new_variables_count += (len(variables) - 1)
    clauses.append([-variables[0], new_variables[0]])
    for i in range(1, len(variables) - 1):
        clauses.append([-variables[i], new_variables[i]])
        clauses.append([-new_variables[i - 1], new_variables[i]])
        clauses.append([-new_variables[i - 1], -variables[i]])
    clauses.append([-new_variables[len(variables) - 2], -variables[len(variables) - 1]])

def exactly_one(n, clauses, variables):
    clauses.append(variables)
    at_most_one(n, clauses, variables)

def generate_clauses(n, variables):
    global new_variables_count
    # ĐÃ SỬA CỰC QUAN TRỌNG: Reset lại đếm biến phụ trợ về 0 cho mỗi lần chạy N mới
    new_variables_count = 0 
    clauses = []

    # Exactly one queen in each row
    for row in range(n):
        exactly_one(n, clauses, variables[row])

    # Exactly one queen in each column
    for col in range(n):
        exactly_one(n, clauses, [variables[row][col] for row in range(n)])

    # At most one queen in each diagonal
    for i in range(1, n):
        diagonal = []
        row = i
        col = 0
        while row >= 0 and col < n:
            diagonal.append(variables[row][col])
            row -= 1
            col += 1
        at_most_one(n, clauses, diagonal)

    for j in range(1, n - 1):
        diagonal = []
        row = n - 1
        col = j
        while row >= 0 and col < n:
            diagonal.append(variables[row][col])
            row -= 1
            col += 1
        at_most_one(n, clauses, diagonal)

    for i in range(n - 1):
        diagonal = []
        row = i
        col = 0
        while row < n and col < n:
            diagonal.append(variables[row][col])
            row += 1
            col += 1
        at_most_one(n, clauses, diagonal)

    for j in range(1, n - 1):
        diagonal = []
        row = 0
        col = j
        while row < n and col < n:
            diagonal.append(variables[row][col])
            row += 1
            col += 1
        at_most_one(n, clauses, diagonal)

    return clauses

# === ĐÃ THÊM HÀM NÀY ĐỂ KẾT NỐI VỚI FILE CHẠY THỰC NGHIỆM ===
def run_sat_solver(n):
    variables = generate_variables(n)
    clauses = generate_clauses(n, variables)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    start_time = time.time()
    solver.solve()
    return time.time() - start_time
# ==============================================================

def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))

# ĐÃ SỬA: Bọc đoạn chạy thử lại để không tự in khi import
if __name__ == "__main__":
    n = 16  # Chạy thử
    variables = generate_variables(n)
    clauses = generate_clauses(n, variables)
    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)
    if solver.solve():
        model = solver.get_model()
        solution = [[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)]
        print_solution(solution)