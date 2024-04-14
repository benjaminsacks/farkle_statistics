import pandas as pd


if __name__ == "__main__":
    # Next Roll
    print("\nExpected value, E(d), for the next roll, given 'd' dice")
    print("Farkle Probability, F(d), for the next roll, given 'd' dice", end="\n\n")

    for d in range(1, 7):
        rolls = pd.read_csv(f"rolls\\{d}_dice_rolls.csv")

        print(f"E({d}) = ", end="")
        print(round((rolls["points"] * rolls["probability"]).sum(), 3), end="\t")
        print(f"F({d}) = ", end="")
        print(round(rolls[rolls["points"] == 0]["probability"].sum() * 100, 1), end="")
        print(" %")

    print()

    # Next Next Roll
