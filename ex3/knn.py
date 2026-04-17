import csv
import math
from collections import Counter

def euclidean(p1, p2):
    return math.sqrt(sum((p1[i] - p2[i])**2 for i in range(len(p1))))

def manhattan(p1, p2):
    return sum(abs(p1[i] - p2[i]) for i in range(len(p1)))

def minmax_normalize(data, n):
    mins = [min(row[i] for row in data) for i in range(n)]
    maxs = [max(row[i] for row in data) for i in range(n)]
    norm_data = []
    for row in data:
        norm_row = [(row[i]-mins[i])/(maxs[i]-mins[i]+1e-9) for i in range(n)]
        norm_data.append(norm_row + [row[-1]])
    return norm_data, mins, maxs

def zscore_normalize(data, n):
    means = [sum(row[i] for row in data)/len(data) for i in range(n)]
    stds = [math.sqrt(sum((row[i]-means[i])**2 for row in data)/len(data)) for i in range(n)]
    norm_data = []
    for row in data:
        norm_row = [(row[i]-means[i])/(stds[i]+1e-9) for i in range(n)]
        norm_data.append(norm_row + [row[-1]])
    return norm_data, means, stds

def read_csv(file):
    data = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if not row: continue
            features = [float(x) for x in row[:-1]]
            label = row[-1].strip()
            data.append(features + [label])
    return data

def main():
    file = input("Enter CSV file name: ")
    raw_data = read_csv(file)
    n = len(raw_data[0]) - 1
    sick_pool = [row for row in raw_data if row[-1].lower() == 'sick']
    healthy_pool = [row for row in raw_data if row[-1].lower() == 'healthy']

    train_raw = sick_pool[:75] + healthy_pool[:75]

    train_ids = [id(r) for r in train_raw]
    test_raw = [r for r in raw_data if id(r) not in train_ids]

    print(f"\n[OK] Training Data: {len(train_raw)} points (75 Sick + 75 Healthy)")
    print(f"[OK] Testing Data: {len(test_raw)} points remaining")

    norm_choice = input("\nSelect Normalization (1: Min-Max, 2: Z-Score): ")

    if norm_choice == '1':
        train_norm, params1, params2 = minmax_normalize(train_raw, n)
        method_name = "Min-Max"
    else:
        train_norm, params1, params2 = zscore_normalize(train_raw, n)
        method_name = "Z-Score"

    print(f"\n--- {method_name} Normalized Training Data (Full 150 Points) ---")
    print(f"{'No':<5} | {'Features':<30} | {'Label'}")
    print("-" * 50)
    for i, row in enumerate(train_norm, 1):
        feat_rounded = [round(x, 4) for x in row[:-1]]
        print(f"{i:<5} | {str(feat_rounded):<30} | {row[-1]}")

    print(f"\nTotal Test Points Available in Pool: {len(test_raw)}")
    indices_str = input(f"Enter test point index numbers (1-{len(test_raw)}) to analyze: ")
    selected_indices = [int(i.strip()) - 1 for i in indices_str.split(',')]

    k = int(input("Enter k value: "))
    dist_choice = input("Select Distance (1: Euclidean, 2: Manhattan): ")
    dist_func = euclidean if dist_choice == '1' else manhattan
    mode = input("Weighted or Unweighted (W/U): ").upper()

    for idx in selected_indices:
        if idx < 0 or idx >= len(test_raw):
            print(f"Index {idx+1} is invalid. Skipping.")
            continue

        test_pt = test_raw[idx]
        test_feat = test_pt[:n]
        actual_label = test_pt[-1]
        if norm_choice == '1':
            norm_test = [(test_feat[i]-params1[i])/(params2[i]-params1[i]+1e-9) for i in range(n)]
        else:
            norm_test = [(test_feat[i]-params1[i])/(params2[i]+1e-9) for i in range(n)]

        print(f"\n>>> Analyzing Test Point {idx+1}: Raw {test_feat} -> Normalized {[round(x,4) for x in norm_test]}")

        distances = []
        for tr_row in train_norm:
            d = dist_func(tr_row[:n], norm_test)
            distances.append((d, tr_row[-1], tr_row[:n]))

        distances.sort(key=lambda x: x[0])
        neighbors = distances[:k]

        print(f"{'Rank':<6}{'Distance':<12}{'Class':<10}{'Norm-Features'}")
        for r, (d, lbl, feat) in enumerate(neighbors, 1):
            feat_round = [round(f, 4) for f in feat]
            print(f"{r:<6}{d:<12.4f}{lbl:<10}{feat_round}")

        if mode == 'U':
            votes = Counter([nbr[1] for nbr in neighbors])
            prediction = votes.most_common(1)[0][0]
        else:
            weights = {}
            for d, lbl, _ in neighbors:
                w = 1 / (d + 1e-5)
                weights[lbl] = weights.get(lbl, 0) + w
            prediction = max(weights, key=weights.get)

        print(f"RESULT: Actual [{actual_label}] | Predicted [{prediction}]")
        print("-" * 70)

if __name__ == "__main__":
    main()
