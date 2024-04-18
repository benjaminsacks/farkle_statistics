import numpy as np
from itertools import combinations


def calculate_max_points(roll) -> tuple[int, int]:
    roll = np.array(roll).astype(int)
    num_dice = len(roll)

    counts = np.zeros(7)
    raw_counts = np.bincount(roll)
    counts[: len(raw_counts)] += raw_counts

    points = 0
    dice_remaining = num_dice

    # Check for six of a kind
    for i in range(1, 7):
        if counts[i] == 6:
            return 3000, 6

    # Check for 1-6 straight
    if np.all(counts[1:] == 1):
        return 1500, 6

    # Check for 3 pairs
    if np.sum(counts == 2) == 3:
        return 1500, 6

    # Check for 2 triplets
    if np.sum(counts == 3) == 2:
        return 2500, 6

    # Check for five of a kind
    for i in range(1, 7):
        if counts[i] == 5:
            points += 2000
            dice_remaining -= 5

            # Check remaining points
            if counts[1] == 1:
                points += 100
                dice_remaining = 6
            if counts[5] == 1:
                points += 50
                dice_remaining = 6

            if dice_remaining == 0:
                return points, 6
            else:
                return points, dice_remaining

    # Check for four of a kind
    for i in range(1, 7):
        if counts[i] == 4:
            points += 1000
            dice_remaining -= 4

            # Check for pair
            for i in range(1, 7):
                if counts[i] == 2:
                    points += 500
                    dice_remaining = 6
                    return points, dice_remaining

            # Check remaining points
            if counts[1] == 1:
                points += 100
                dice_remaining -= 1
            if counts[5] == 1:
                points += 50
                dice_remaining -= 1

            if dice_remaining == 0:
                return points, 6
            else:
                return points, dice_remaining

    # Check for three of a kind
    for i in range(1, 7):
        if counts[i] == 3:
            if i == 1:
                points += 300
            else:
                points += i * 100
            dice_remaining -= 3

            # Check remaining points
            if counts[1] in (1, 2):
                points += 100 * counts[1]
                dice_remaining -= counts[1]
            if counts[5] in (1, 2):
                points += 50 * counts[5]
                dice_remaining -= counts[5]

            if dice_remaining == 0:
                return points, 6
            else:
                return points, dice_remaining

    # Check remaining points
    if counts[1] in (1, 2):
        points += 100 * counts[1]
        dice_remaining -= counts[1]
    if counts[5] in (1, 2):
        points += 50 * counts[5]
        dice_remaining -= counts[5]

    if points == 0:
        return 0, 0
    elif dice_remaining == 0:
        return points, 6
    else:
        return points, dice_remaining


def calculate_possible_points(roll):
    point_options = {}

    for d in range(len(roll)):
        for r in set(combinations(roll, d + 1)):
            max_points, dice_remaining = calculate_max_points(r)
            if max_points == 0:
                continue
            if dice_remaining == 6 and len(r) < len(roll):
                dice_remaining = 0
            
            if max_points not in point_options:
                point_options[int(max_points)] = len(roll) - len(r) + dice_remaining
            else:
                point_options[max_points] = max(
                    point_options[max_points], (len(roll) - len(r) + dice_remaining)
                )

    return [(key, value) for key, value in point_options.items()]


if __name__ == "__main__":
    # roll = [2, 2, 3, 3, 4, 6]
    roll = [1, 1, 1, 2, 2, 2]
    # roll = [1, 5, 5]
    points, dice_remaining = calculate_max_points(roll)
    print(roll)
    print("Maximum points:", points)
    print("Dice remaining:", dice_remaining)

    print(sorted(list(calculate_possible_points(roll))))
