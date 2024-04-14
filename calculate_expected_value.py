import pandas as pd
from calculate_points import calculate_possible_points


def select_max_points(possible_points, ev_base, current_points=0):
    if len(possible_points) == 0:
        return False, 0

    max_roll = 0
    for points, remaining_dice in possible_points:
        ev_roll = points + ev_base[remaining_dice]

        if ev_roll > max_roll:
            selected_points = points
            selected_remaining_dice = remaining_dice
            max_roll = ev_roll

    reroll = False
    if ev_base[selected_remaining_dice] > current_points + selected_points:
        reroll = True
        current_points += max_roll
    else:
        current_points += selected_points

    return reroll, current_points, selected_points, selected_remaining_dice


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

            # if d == 1:
            #     print(roll, end="\t")
            #     print(select_max_points(calculate_possible_points(roll), ev_base))

            ev_l2[d] += (
                r.iloc[-1]
                * select_max_points(calculate_possible_points(roll), ev_base)[1]
            )

        print(f"E({d}) = " + str(round(ev_l2[d], 3)))
    print()


    # Next Next Next Roll
    ev_l3 = {i: 0 for i in range(1, 7)}
    for d in range(1, 7):
        rolls = pd.read_csv(f"rolls\\{d}_dice_rolls.csv")
        for _, r in rolls.iterrows():
            roll = list(r.iloc[:-3])

            # if d == 1:
            #     print(roll, end="\t")
            #     print(select_max_points(calculate_possible_points(roll), ev_base))

            ev_l3[d] += (
                r.iloc[-1]
                * select_max_points(calculate_possible_points(roll), ev_l2)[1]
            )

        print(f"E({d}) = " + str(round(ev_l3[d], 3)))
    print()
