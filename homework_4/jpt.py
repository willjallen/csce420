from itertools import product
from typing import List, Tuple

# Define the probability tables provided in the data
P_Cold = {False: 0.95, True: 0.05}
P_Cat = {False: 0.98, True: 0.02}
P_Allergy_given_Cat = {(False, False): 0.95, (False, True): 0.05, (True, False): 0.25, (True, True): 0.75}
P_Sneeze_given_Cold_Allergy = {(False, False, False): 0.99, (False, False, True): 0.01, 
                               (False, True, False): 0.30, (False, True, True): 0.70, 
                               (True, False, False): 0.20, (True, False, True): 0.80, 
                               (True, True, False): 0.10, (True, True, True): 0.90}
P_Scratches_given_Cat = {(False, False): 0.95, (False, True): 0.05, (True, False): 0.50, (True, True): 0.50}

# Define all possible combinations of truth values for the variables
combinations = list(product([False, True], repeat=5))

# Calculate the joint probability for each combination
def calculate_joint_prob(combinations: List[Tuple[bool]]) -> List[Tuple[Tuple[bool], float]]:
    joint_prob_table = []
    for combo in combinations:
        cold, allergy, cat, sneeze, scratches = combo
        joint_prob = (P_Cold[cold] * P_Cat[cat] * P_Allergy_given_Cat[cat, allergy] *
                      P_Sneeze_given_Cold_Allergy[cold, allergy, sneeze] * P_Scratches_given_Cat[cat, scratches])
        joint_prob_table.append((combo, joint_prob))
    return joint_prob_table


def print_table(joint_prob_table: List[Tuple[Tuple[bool], float]]):
    # Initialize table header
    header = ("Cold", "Allergy", "Cat", "Sneeze", "Scratches", "Joint Probability")
    # Create the LaTeX table structure
    latex_table = "\\begin{table}[h!]\n"
    latex_table += "\\centering\n"
    latex_table += "\\begin{tabular}{|c|c|c|c|c|c|}\n"
    latex_table += "\\hline\n"
    # Add table header to LaTeX table
    latex_table += " & ".join(header) + " \\\\ \\hline\n"
    # Add rows to the table
    for combo, joint_prob in joint_prob_table:
        cold, allergy, cat, sneeze, scratches = combo
        # Convert boolean values to text
        cold_text = "True" if cold else "False"
        allergy_text = "True" if allergy else "False"
        cat_text = "True" if cat else "False"
        sneeze_text = "True" if sneeze else "False"
        scratches_text = "True" if scratches else "False"
        # Add row to LaTeX table
        row = (cold_text, allergy_text, cat_text, sneeze_text, scratches_text, f"{joint_prob:.5f}")
        latex_table += " & ".join(row) + " \\\\ \\hline\n"
    # Close tabular and table environments
    latex_table += "\\end{tabular}\n"
    latex_table += "\\end{table}"
    print(latex_table)


joint_prob_table = calculate_joint_prob(combinations)
print_table(joint_prob_table)

jpt = dict(calculate_joint_prob(combinations))

# Calculate P(allergic, sneeze, ¬cold, scratches) and P(sneeze, ¬cold, scratches)
p_allergic_sneeze_not_cold_scratches = sum([jpt[(False, True, cat, True, True)] for cat in [False, True]])
p_sneeze_not_cold_scratches = sum([jpt[(False, allergic, cat, True, True)] for cat in [False, True] for allergic in [False, True]])

# Calculate P(allergic | sneeze, ¬cold, scratches)
p_allergic_given_sneeze_not_cold_scratches = p_allergic_sneeze_not_cold_scratches / p_sneeze_not_cold_scratches
print(f"P(allergic | sneeze, ¬cold, scratches) = {p_allergic_given_sneeze_not_cold_scratches}")

