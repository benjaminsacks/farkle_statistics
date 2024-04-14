import numpy as np
import math
from itertools import combinations_with_replacement
from calculate_points import calculate_points
from count_permutations import count_permutations

if __name__ == "__main__":
    for d in range(1, 7):
        rolls = combinations_with_replacement(list(range(1, 7)), d)
        num_rolls = int(
            (math.factorial(d + 5)) / (math.factorial(d) * math.factorial(5))
        )

        rolls_points_perms = np.zeros(shape=(num_rolls, d + 2))
        for i, r in enumerate(rolls):
            rolls_points_perms[i][:d] = r
            rolls_points_perms[i][d] = calculate_points(r)[0]
            rolls_points_perms[i][d + 1] = count_permutations(r, d) / num_rolls

        np.savetxt(f"rolls\\{d}_dice_rolls.csv", rolls_points_perms, delimiter=",")
