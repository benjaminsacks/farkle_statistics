import numpy as np

def calculate_points(roll):
    roll = np.array(roll).astype(int)
    counts = np.zeros(7)
    raw_counts = np.bincount(roll)
    counts[:len(raw_counts)] += raw_counts
    
    points = 0
    dice_remaining = 6

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

            if dice_remaining == 0: return points, 6
            else: return points, dice_remaining
    
    # Check for three of a kind
    for i in range(1, 7):
        if counts[i] == 3:
            if i == 1: points += 300
            else: points += i * 100
            dice_remaining -= 3

            # Check remaining points
            if counts[1] in (1, 2): 
                points += 100 * counts[1]
                dice_remaining -= counts[1]
            if counts[5] in (1, 2): 
                points += 50 * counts[5]
                dice_remaining -= counts[5]

            if dice_remaining == 0: return points, 6
            else: return points, dice_remaining
    
    # Check remaining points
    if counts[1] in (1, 2): 
        points += 100 * counts[1]
        dice_remaining -= counts[1]
    if counts[5] in (1, 2): 
        points += 50 * counts[5]
        dice_remaining -= counts[5]

    if points == 0: return 0, 0
    elif dice_remaining == 0: return points, 6
    else: return points, dice_remaining

if __name__ == "__main__":
    roll = [1, 1, 1, 1, 1, 1]
    points, dice_remaining = calculate_points(roll)
    print(roll)
    print("Maximum points:", points)
    print("Dice remaining:", dice_remaining)