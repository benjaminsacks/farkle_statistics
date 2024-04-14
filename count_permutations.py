import numpy as np
import math

def count_permutations(roll, num_dice):
    np.array(roll).astype(int)
    counts = np.bincount(roll)

    numerator = math.perm(num_dice, num_dice)
    denominator = 1

    for i in counts:
        if i > 1:
            denominator *= math.factorial(i)


    return int(numerator / denominator)

if __name__ == "__main__":
    roll = [1, 2, 3, 4, 5, 5]
    print(f"# of permutations of {roll}: " + str(count_permutations(roll)))