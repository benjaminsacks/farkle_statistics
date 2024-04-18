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


def squash_list(lst):
    return "".join(map(str, lst))


def filter_pp(possible_points):
    point_options = {}

    for p, d in possible_points:
        if d not in point_options:
            point_options[d] = p
        else:
            point_options[d] = max(point_options[d], p)

    return [(value, key) for key, value in point_options.items()]


choices = {}
for d in range(1, 7):
    rolls = pd.read_csv(f"rolls\\{d}_dice_rolls.csv")
    for _, r in rolls.iterrows():
        roll = [int(s) for s in r.iloc[:-3]]
        possible_points = filter_pp(calculate_possible_points(roll))

        choices[squash_list(roll)] = [
            {"points": p, "remaining_dice": d} for p, d in possible_points
        ]

# Write data to a file
with open("choices.json", "w") as json_file:
    json.dump(choices, json_file, indent=4)
