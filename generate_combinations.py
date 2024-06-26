import numpy as np
import pandas as pd
import math
from itertools import combinations_with_replacement
from calculate_points import calculate_max_points
from count_permutations import count_permutations

if __name__ == "__main__":
    for d in range(1, 7):
        rolls = combinations_with_replacement(list(range(1, 7)), d)
        num_rolls = int(
            (math.factorial(d + 5)) / (math.factorial(d) * math.factorial(5))
        )

        rolls_points_perms = np.zeros(shape=(num_rolls, d + 3))
        for i, r in enumerate(rolls):
            rolls_points_perms[i][:d] = r
            rolls_points_perms[i][[d, d + 1]] = calculate_max_points(r)
            rolls_points_perms[i][d + 2] = count_permutations(r, d) / 6**d

        column_names = [f"d{n}" for n in range(1, d + 1)] + [
            "points",
            "dice_remaining",
            "probability",
        ]
        df = pd.DataFrame(rolls_points_perms, columns=column_names)
        df.iloc[:, :-1] = df.iloc[:, :-1].astype(int)

        df.to_csv(f"rolls\\{d}_dice_rolls.csv", index=False)
