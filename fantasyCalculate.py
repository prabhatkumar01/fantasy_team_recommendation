import pandas as pd

# Player innings data
data = [
    ["DA Warner", "yes", 29, 21, 3, 2, 138.09, True],
    ["MR Marsh", "yes", 20, 12, 2, 2, 166.66, True],
    ["SD Hope", "yes", 33, 25, 2, 2, 132, True],
    ["RR Pant", "yes", 18, 13, 2, 0, 138.46, True],
    ["RK Bhui", "yes", 3, 7, 0, 0, 42.85, True],
    ["T Stubbs", "yes", 5, 8, 0, 0, 62.5, True],
    ["AR Patel", "yes", 21, 13, 2, 1, 161.53, True],
    ["Sumit Kumar", "yes", 2, 9, 0, 0, 22.22, True],
    ["Abishek Porel", "yes", 32, 10, 4, 2, 320, False],
    ["Kuldeep Yadav", "yes", 1, 2, 0, 0, 50, True],
    ["KK Ahmed", "DNB", None, None, None, None, None, False],
    ["I Sharma", "DNB", None, None, None, None, None, False],
    ["Arshdeep Singh", "sub", None, None, None, None, None, False],
    ["S Dhawan", "yes", 22, 16, 4, 0, 137.5, True],
    ["JM Bairstow", "yes", 9, 3, 2, 0, 300, True],
    ["Prabhsimran Singh", "yes", 26, 17, 5, 0, 152.94, True],
    ["SM Curran", "yes", 63, 47, 6, 1, 134.04, True],
    ["JM Sharma", "yes", 9, 9, 1, 0, 100, True],
    ["LS Livingstone", "yes", 38, 21, 2, 3, 180.95, False],
    ["Shashank Singh", "yes", 0, 1, 0, 0, 0, True],
    ["Harpreet Brar", "yes", 2, 2, 0, 0, 100, False],
    ["HV Patel", "DNB", None, None, None, None, None, False],
    ["K Rabada", "DNB", None, None, None, None, None, False],
    ["RD Chahar", "DNB", None, None, None, None, None, False],
]

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Name", "Batted Type", "Runs", "Balls", "Fours", "Sixes", "Strike Rate", "Out"])

# Function to calculate fantasy points
def calculate_fantasy_points(row):
    if row["Batted Type"] == "DNB":  # Did Not Bat
        return 0

    points = 0
    
    # Runs
    if row["Runs"] is not None:
        points += row["Runs"]  # 1 point per run
        points += row["Fours"]  # 1 extra point per four
        points += row["Sixes"] * 2  # 2 extra points per six

    # Strike Rate Bonus
    if row["Balls"] and row["Balls"] >= 10:  # Minimum balls faced for SR bonus
        sr = row["Strike Rate"]
        if sr >= 170:
            points += 6
        elif 150 <= sr < 170:
            points += 4
        elif 130 <= sr < 150:
            points += 2
        elif 60 <= sr < 70:
            points -= 2
        elif 50 <= sr < 60:
            points -= 4
        elif sr < 50:
            points -= 6

    # Duck Penalty (if out and made 0 runs)
    if row["Out"] and row["Runs"] == 0:
        points -= 2

    return points

# Apply function
df["Fantasy Points"] = df.apply(calculate_fantasy_points, axis=1)

# Display results
print(df[["Name", "Fantasy Points"]])

