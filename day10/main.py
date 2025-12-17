from itertools import combinations
from functools import lru_cache
import numpy as np
from scipy.optimize import nnls
from z3 import Int, Solver, Sum, sat  # Add this import at the top
switcheroo = {"#": ".", ".": "#"}



def apply_button(state, button_wiring):
   """Apply a button press to the current state"""
   new_state = state.copy()
   for idx_str in button_wiring:
      idx = int(idx_str)
      new_state[idx] = switcheroo[new_state[idx]]
   return new_state

def find_button_combinations(initial_state, target_state, buttons):
   """Find all combinations of button presses that reach target state"""
   n_buttons = len(buttons)
   valid_combinations = []
   seen_states = set()
   
   # Try all possible combinations of button presses (up to all buttons)
   for r in range(1, n_buttons + 1):
      for combo in combinations(range(n_buttons), r):
         # Apply buttons in the combination
         state = initial_state.copy()
         
         for button_idx in combo:
               state = apply_button(state, buttons[button_idx])
         
         # Check if we reached target state and combination is unique
         state_tuple = tuple(state)
         if state == target_state and state_tuple not in seen_states:
               seen_states.add(state_tuple)
               valid_combinations.append((combo, len(combo)))
   
   return valid_combinations

def apply_jbutton(state, button_wiring):
   """Apply a button press to the current state"""
   new_state = state.copy()
   for idx_str in button_wiring:
      idx = int(idx_str)
      new_state[idx] += 1 
   return new_state

def find_joltage_combinations(initial_state, target_state, buttons):
   """Find minimum button presses by solving system of equations"""
   import numpy as np
   
   n_buttons = len(buttons)
   n_positions = len(target_state)
   
   # Build matrix: each row is a position, each column is a button
   A = np.zeros((n_positions, n_buttons), dtype=float)
   for btn_idx, wiring in enumerate(buttons):
      for idx_str in wiring:
         idx = int(idx_str)
         if idx < n_positions:
            A[idx][btn_idx] = 1
   
   b = np.array(target_state, dtype=float)
   
   # Solve using least squares with non-negative constraint

   
   solution, residual = nnls(A, b)
   
   # Round to nearest integer
   solution = np.round(solution).astype(int)
   
   # Verify solution
   result = A @ solution
   if np.allclose(result, b):
      return [(tuple(solution), int(sum(solution)))]
   
   # If nnls doesn't work, try iterative refinement
   # Start with nnls solution and adjust
   solution = list(solution)
   remaining = [target_state[p] - int(sum(A[p][btn] * solution[btn] for btn in range(n_buttons))) for p in range(n_positions)]
   
   # Greedy fix
   max_iter = 1000
   for _ in range(max_iter):
      if all(r == 0 for r in remaining):
         break
      
      # Find position with most remaining
      pos = max(range(n_positions), key=lambda p: remaining[p])
      if remaining[pos] <= 0:
         break
      
      # Find button that affects this position
      for btn_idx in range(n_buttons):
         if A[pos][btn_idx] == 1:
            # Check if pressing this button is valid
            can_press = True
            for p in range(n_positions):
               if A[p][btn_idx] == 1 and remaining[p] <= 0:
                  can_press = False
                  break
            if can_press:
               solution[btn_idx] += 1
               for p in range(n_positions):
                  if A[p][btn_idx] == 1:
                     remaining[p] -= 1
               break
   
   if all(r == 0 for r in remaining):
      return [(tuple(solution), sum(solution))]
   return []

def find_joltage_combinations_z3(initial_state, target_state, buttons):
    """Find minimum button presses using Z3 SMT solver"""
    n_buttons = len(buttons)
    n_positions = len(target_state)
    # Variables: how many times to press each button
    presses = [Int(f"b{i}") for i in range(n_buttons)]
    s = Solver()
    # Each press count must be >= 0
    for p in presses:
        s.add(p >= 0)
    # For each position, sum of button effects must equal target
    for pos in range(n_positions):
        effect = Sum([presses[btn_idx] if str(pos) in buttons[btn_idx] else 0 for btn_idx in range(n_buttons)])
        s.add(effect == target_state[pos])
    # Minimize total presses
    total_presses = Sum(presses)
    min_presses = None
    best_solution = None
    # Iteratively search for minimal solution
    for guess in range(sum(target_state)+1):
        s.push()
        s.add(total_presses == guess)
        if s.check() == sat:
            m = s.model()
            best_solution = tuple(m.evaluate(p).as_long() for p in presses)
            min_presses = guess
            s.pop()
            break
        s.pop()
    if best_solution is not None:
        return [(best_solution, min_presses)]
    return []


def main():
    machines = []
    with open("input.txt") as f:
      for line in f:
            line = line.strip().split(" ")
            indicator_lights = [x for x in line[0][1:-1]]
            button_wirings = [x.replace("(", "").replace(")","").split(",") for x in line[1:-1]]
            joltage = [int(x) for x in line[-1][1:-1].split(",")]
            machines.append([indicator_lights, button_wirings, joltage])
      
      #part 1      
      min_presses = 0
      for m in machines:
         indicator_lights, button_wirings, _ = m
         initial_state = ['.'] * len(indicator_lights)

         combinations = find_button_combinations(initial_state, indicator_lights, button_wirings)

         presses = [x[-1] for x in combinations]

         if combinations:
            # Find minimum number of button presses
            min_presses += min(presses)
            
      print(f"Minimum button presses: {min_presses}")

      #part 2
      min_presses_p2 = 0
      for m in machines:
         _, button_wirings, joltage = m
         initial_state = [0] * len(joltage)

         combinations = find_joltage_combinations_z3(initial_state, joltage, button_wirings)

         if combinations:
            # Find minimum button presses
            valid_presses = [x[-1] for x in combinations]
            min_presses_p2 += min(valid_presses)
      print(f"Minimum button presses (part 2): {min_presses_p2}")
        
main()
