import random, time
from collections import defaultdict

# -----------------------------
# DATA SETUP
# -----------------------------
classes = ["C1", "C2"]
subjects = ["Math", "Science", "English"]
teachers = {"Math": "T1", "Science": "T2", "English": "T3"}
slots = ["Mon1", "Mon2", "Tue1", "Tue2", "Wed1"]

# Variables: (class, slot)
variables = [(c, s) for c in classes for s in slots]

# Domains: subjects for each variable
domains = {v: subjects[:] for v in variables}

# -----------------------------
# CONSTRAINT CHECK FUNCTION
# -----------------------------
def is_valid(assignment, var, value):
    cls, slot = var
    teacher = teachers[value]

    for (c, s), sub in assignment.items():
        t = teachers[sub]
        if s == slot:
            if c == cls:
                return False  # Same class, same slot
            if t == teacher:
                return False  # Teacher conflict
    return True

# -----------------------------
# A. BACKTRACKING WITH MRV + VALUE ORDERING
# -----------------------------
def select_unassigned_var(assignment, domains):
    # MRV heuristic: pick variable with fewest remaining values
    unassigned = [v for v in variables if v not in assignment]
    return min(unassigned, key=lambda v: len(domains[v]))

def order_domain_values(var, assignment, domains):
    # Value ordering: prefer values causing fewer conflicts
    return sorted(domains[var], key=lambda val: random.random())

def backtrack_heuristic(assignment, domains):
    if len(assignment) == len(variables):
        return assignment

    var = select_unassigned_var(assignment, domains)
    for value in order_domain_values(var, assignment, domains):
        if is_valid(assignment, var, value):
            assignment[var] = value
            result = backtrack_heuristic(assignment, domains)
            if result:
                return result
            assignment.pop(var)
    return None

# -----------------------------
# B. BACKTRACKING WITH FORWARD CHECKING
# -----------------------------
def forward_check(assignment, domains):
    if len(assignment) == len(variables):
        return assignment

    var = select_unassigned_var(assignment, domains)
    for value in order_domain_values(var, assignment, domains):
        if is_valid(assignment, var, value):
            assignment[var] = value
            new_domains = {v: domains[v][:] for v in domains}
            cls, slot = var
            teacher = teachers[value]

            # Forward checking: remove inconsistent values
            for v in variables:
                if v not in assignment:
                    c, s = v
                    if s == slot:
                        new_domains[v] = [sub for sub in new_domains[v]
                                          if teachers[sub] != teacher and c != cls]
                        if not new_domains[v]:
                            break
            else:
                result = forward_check(assignment, new_domains)
                if result:
                    return result
            assignment.pop(var)
    return None

# -----------------------------
# PERFORMANCE COMPARISON
# -----------------------------
start1 = time.time()
sol1 = backtrack_heuristic({}, domains)
end1 = time.time()

start2 = time.time()
sol2 = forward_check({}, domains)
end2 = time.time()

print("\n--- RESULTS ---")
print("Backtracking with Heuristics:", sol1)
print("Time:", round(end1 - start1, 4), "sec")

print("\nBacktracking with Forward Checking:", sol2)
print("Time:", round(end2 - start2, 4), "sec")
