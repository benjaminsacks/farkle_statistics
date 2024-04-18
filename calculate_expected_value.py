import pandas as pd
from calculate_points import calculate_max_points
from calculate_points import calculate_possible_points
import json


def select_max_points(possible_points, expected_values, round_points):
    if len(possible_points) == 0:  # if Farkle
        return 0, 0, False, 0

    max_roll = 0
    for points, remaining_dice in possible_points:
        ev_roll = points + expected_values[remaining_dice]

        if ev_roll > max_roll:
            selected_points = points
            selected_remaining_dice = remaining_dice
            max_roll = ev_roll

    if expected_values[selected_remaining_dice] > round_points + selected_points:
        reroll = True
        round_points += max_roll
    else:
        reroll = False
        round_points += selected_points

    return selected_points, selected_remaining_dice, reroll, round_points


def ev_base_to_json():
    ev_base = {}
    for d in range(1, 7):
        rolls = pd.read_csv(f"rolls\\{d}_dice_rolls.csv")
        ev_base[d] = round((rolls["points"] * rolls["probability"]).sum(), 3)

    # Write data to a file
    with open("ev_base.json", "w") as json_file:
        json.dump(ev_base, json_file, indent=4)


def squash_list(lst):
    return "".join(map(str, [int(i) for i in lst]))


def filter_possible_points(possible_points):
    point_options = {}

    for p, d in possible_points:
        if d not in point_options:
            point_options[d] = p
        else:
            point_options[d] = max(point_options[d], p)

    return [(value, key) for key, value in point_options.items()]


def choices_to_json():
    choices = {}
    for d in range(1, 7):
        rolls = pd.read_csv(f"rolls\\{d}_dice_rolls.csv")
        for _, r in rolls.iterrows():
            roll = [int(s) for s in r.iloc[:-3]]
            possible_points = filter_possible_points(calculate_possible_points(roll))

            choices[squash_list(roll)] = [
                {"points": p, "remaining_dice": d} for p, d in possible_points
            ]

    # Write data to a file
    with open("choices.json", "w") as json_file:
        json.dump(choices, json_file, indent=4)


def expected_value(d, depth=1, points=0):
    if depth <= 0:  # Stop condition
        with open("ev_base.json", "r") as file:
            ev_base = json.load(file)
        return ev_base[str(int(d))] + points

    rolls = pd.read_csv(f"rolls\\{d}_dice_rolls.csv")
    with open("choices.json", "r") as file:
        choices = json.load(file)

    ev = 0
    for _, r in rolls.iterrows():
        roll_choices = choices[squash_list(list(r.iloc[:-3]))]
        # if len(roll_choices) == 0:  # If Farkle
        #     return

        choice_evs = [0]
        for c in roll_choices:
            choice_evs += [points + expected_value(c["remaining_dice"], depth - 1, c["points"])]

        ev += r.iloc[-1] * max(choice_evs)

    return ev


if __name__ == "__main__":
    # Next Roll
    print("\nExpected value, E(d), for the next roll, given 'd' dice")
    print("Farkle Probability, F(d), for the next roll, given 'd' dice", end="\n\n")

    ev_base = {}
    fp_base = {}

    for d in range(1, 7):
        rolls = pd.read_csv(f"rolls\\{d}_dice_rolls.csv")

        ev_base[d] = (rolls["points"] * rolls["probability"]).sum()
        fp_base[d] = rolls[rolls["points"] == 0]["probability"].sum()

        print(f"E({d}) = " + str(round(ev_base[d], 3)), end="\t")
        print(f"F({d}) = " + str(round(fp_base[d] * 100, 1)) + "%")

    ev_base_to_json()
    print()

    # Next Next Roll
    ev_l2 = {i: 0 for i in range(1, 7)}
    for d in range(1, 7):
        rolls = pd.read_csv(f"rolls\\{d}_dice_rolls.csv")
        for _, r in rolls.iterrows():
            roll = list(r.iloc[:-3])

            ev_l2[d] += (
                r.iloc[-1]
                * select_max_points(calculate_possible_points(roll), ev_base, 0)[3]
            )

        print(f"E({d}) = " + str(round(ev_l2[d], 3)))
    print()

    # "Infinite" Rolls (max_depth)
    for d in range(1, 7):
        print(f"E({d}): " + str(expected_value(d)))
