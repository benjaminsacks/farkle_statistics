import pandas as pd
from calculate_points import calculate_possible_points
import json

# for d in range(1, 7):
#     rolls = pd.read_csv(f"rolls\\{d}_dice_rolls.csv")

#     p = {}
#     for i in range(7):
#         p[i] = rolls[rolls["dice_remaining"] == i]["probability"].sum()

#     print(f"{d} dice roll")
#     [print(f"F({i}) = " + str(round(p[i] * 100, 1)), end="%\t") for i in range(7)]
#     print("\n")


with open("choices.json", "r") as file:
    choices = json.load(file)

[print(c['points']) for c in choices['111']]
