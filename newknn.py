import csv
import math
from collections import Counter, defaultdict

# ---------------------------
# DISTANCE FUNCTIONS
# ---------------------------
def euclidean(p1, p2):
    return math.sqrt(sum((p1[i] - p2[i]) ** 2 for i in range(len(p1))))

def manhattan(p1, p2):
    return sum(abs(p1[i] - p2[i]) for i in range(len(p1)))

# ---------------------------
# MIN-MAX NORMALIZATION
# ---------------------------
def minmax_normalize(data, n):
    mins = [min(row[i] for row in data) for i in range(n)]
    maxs = [max(row[i] for row in data) for i in range(n)]

    norm = []
    for row in data:
        new_row = [
            (row[i] - mins[i]) / (maxs[i] - mins[i] + 1e-9)
            for i in range(n)
        ]
        norm.append(new_row + [row[-1]])

    return norm, mins, maxs

# ---------------------------
# Z-SCORE NORMALIZATION
# ---------------------------
def zscore_normalize(data, n):
    means = [sum(row[i] for row in data) / len(data) for i in range(n)]

    stds = [
        math.sqrt(sum((row[i] - means[i]) ** 2 for row in data) / len(data))
        for i in range(n)
    ]

    norm = []
    for row in data:
        new_row = [
            (row[i] - means[i]) / (stds[i] + 1e-9)
            for i in range(n)
        ]
        norm.append(new_row + [row[-1]])

    return norm, means, stds

# ---------------------------
# READ CSV
# ---------------------------
def read_csv(file):
    data = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            features = [float(x) for x in row[:-1]]
            label = row[-1].strip()
            data.append(features + [label])

    return data

# ---------------------------
# MAIN
# ---------------------------
def main():

    file = input("Enter CSV file name: ")
    raw_data = read_csv(file)

    n = len(raw_data[0]) - 1

    # ---------------------------
    # STRATIFIED SPLIT
    # ---------------------------
    class_groups = defaultdict(list)

    for row in raw_data:
        class_groups[row[-1]].append(row)

    train_raw = []
    for label, rows in class_groups.items():
        split = int(0.5 * len(rows))
        train_raw += rows[:split]

    train_ids = set(id(r) for r in train_raw)
    test_raw = [r for r in raw_data if id(r) not in train_ids]

    print("\nTrain size:", len(train_raw))
    print("Test size:", len(test_raw))

    # ---------------------------
    # NORMALIZATION
    # ---------------------------
    norm_choice = input("\n1: Min-Max  2: Z-Score: ")

    if norm_choice == '1':
        train_norm, p1, p2 = minmax_normalize(train_raw, n)
        method = "Min-Max"
    else:
        train_norm, p1, p2 = zscore_normalize(train_raw, n)
        method = "Z-Score"

    print(f"\n--- {method} TRAIN DATA ---")
    for i, row in enumerate(train_norm[:5], 1):
        print(i, [round(x, 3) for x in row[:-1]], row[-1])

    # ---------------------------
    # TEST INPUT
    # ---------------------------
    idx = int(input("\nEnter test index: "))
    k = int(input("Enter K: "))
    dist_choice = input("1: Euclidean  2: Manhattan: ")
    mode = input("W: Weighted / U: Unweighted: ").upper()

    dist_func = euclidean if dist_choice == '1' else manhattan

    # ---------------------------
    # TEST POINT
    # ---------------------------
    test_pt = test_raw[idx]
    test_feat = test_pt[:n]
    actual = test_pt[-1]

    if norm_choice == '1':
        norm_test = [(test_feat[i] - p1[i]) / (p2[i] - p1[i] + 1e-9) for i in range(n)]
    else:
        norm_test = [(test_feat[i] - p1[i]) / (p2[i] + 1e-9) for i in range(n)]

    print("\nTest Point:", [round(x, 3) for x in norm_test])

    # ---------------------------
    # DISTANCE CALCULATION
    # ---------------------------
    distances = []

    for tr in train_norm:
        d = dist_func(tr[:n], norm_test)
        distances.append((d, tr[-1]))

    distances.sort(key=lambda x: x[0])
    neighbors = distances[:k]

    print("\n--- NEIGHBORS ---")
    for i, (d, lbl) in enumerate(neighbors, 1):
        print(i, round(d, 4), lbl)

    # ---------------------------
    # VOTING
    # ---------------------------
    if mode == 'U':
        votes = Counter([n[1] for n in neighbors])
        prediction = votes.most_common(1)[0][0]

    else:
        weights = {}
        for d, lbl in neighbors:
            w = 1 / (d + 1e-5)
            weights[lbl] = weights.get(lbl, 0) + w

        prediction = max(weights, key=weights.get)

    # ---------------------------
    # RESULT
    # ---------------------------
    print("\n====================")
    print("ACTUAL:", actual)
    print("PREDICTED:", prediction)
    print("====================")

    if actual == prediction:
        print("✔ CORRECT")
    else:
        print("✘ WRONG")


if __name__ == "__main__":
    main()
