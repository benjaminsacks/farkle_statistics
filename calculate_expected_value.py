import pandas as pd
from calculate_points import calculate_possible_points


def select_max_points(possible_points, expected_values, round_points):
    if len(possible_points) == 0: # if Farkle
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

def check_all_subrolls(roll, depth):
    if calculate_possible_points(roll)[0] == 0:
        return
    
    for r in calculate_possible_points(roll):
        pass
    pass


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
    max_depth = 2

    dice_rolls = {}
    for d in range(1, 7):
        dice_rolls[d] = pd.read_csv(f"rolls\\{d}_dice_rolls.csv")

    ev_optimal = {i: 0 for i in range(1, 7)}
    for d in range(1, 7):
        rolls = pd.read_csv(f"rolls\\{d}_dice_rolls.csv")
        for _, r in rolls.iterrows():
            roll = list(r.iloc[:-3])