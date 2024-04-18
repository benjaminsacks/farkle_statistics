import numpy as np
import pandas as pd
from calculate_points import calculate_max_points
from calculate_points import calculate_possible_points
from calculate_expected_value import select_max_points

from tqdm import tqdm

if __name__ == "__main__":
    m = 20  # Number of entries in 'Expected Value' dataframe
    n = 1_000  # Number of simulations per dice
    layer = -1

    if layer == 1:
        for d in range(1, 7):
            point_sum = 0
            for _ in range(n):
                roll = np.random.choice(6, d) + np.ones(d)
                point_sum += calculate_max_points(roll)[0]

            print(f"\u03bc{d} = " + str(point_sum / n))

    if layer == 2:
        ev_base = {}
        for d in range(1, 7):
            rolls = pd.read_csv(f"rolls\\{d}_dice_rolls.csv")
            ev_base[d] = (rolls["points"] * rolls["probability"]).sum()

        for d in range(1, 7):
            point_sum = 0
            for _ in range(n):
                roll = np.random.choice(6, d) + np.ones(d)  # First roll
                if calculate_max_points(roll)[0] > 0:  # If not a farkle
                    possible_points = calculate_possible_points(roll)
                    roll_choice = select_max_points(
                        possible_points, ev_base, 0
                    )  # ~Optimal~ choice

                    round_points = roll_choice[0]  # Add selected points to round total
                    if roll_choice[2]:  # If reroll == True
                        roll_2 = np.random.choice(6, roll_choice[1]) + np.ones(
                            roll_choice[1]
                        )
                        if calculate_max_points(roll_2)[0] > 0:  # If not a farkle
                            possible_points_2 = calculate_possible_points(roll_2)
                            roll_choice_2 = select_max_points(
                                possible_points_2, ev_base, round_points
                            )  # ~Optimal~ choice
                            round_points += roll_choice_2[
                                0
                            ]  # Add selected points to round total
                        else:
                            round_points = 0
                else:
                    round_points = 0

                point_sum += round_points

            print(f"\u03bc{d} = " + str(point_sum / n))

    if layer == -1:
        ev_df = pd.DataFrame(columns=list(range(1, 7)))

        ev_row = []
        for d in range(1, 7):
            rolls = pd.read_csv(f"rolls\\{d}_dice_rolls.csv")
            ev_row += [(rolls["points"] * rolls["probability"]).sum()]
        ev_df.loc[0] = ev_row

        with tqdm(total=6 * m - 6) as pbar:
            for i in range(1, m):
                ev_row = []
                for d in range(1, 7):
                    point_sum = 0
                    for _ in range(n):
                        round_points = 0  # Initial state
                        reroll = True
                        num_dice = d

                        while reroll:
                            roll = np.random.choice(6, num_dice) + np.ones(num_dice)
                            if calculate_max_points(roll)[0] == 0:  # If farkle
                                round_points = 0
                                break

                            possible_points = calculate_possible_points(roll)
                            roll_choice = select_max_points(
                                possible_points, ev_df.loc[i - 1], round_points
                            )  # Optimal

                            round_points += roll_choice[
                                0
                            ]  # Add selected points to round total
                            num_dice = roll_choice[1]
                            reroll = roll_choice[2]

                        point_sum += round_points

                    ev_row += [point_sum / n]
                    pbar.update(1)
                ev_df.loc[i] = ev_row

        ev_df.to_csv("expected_values.csv", index=False)
