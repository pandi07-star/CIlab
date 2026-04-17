data = []
with open("data.txt", "r") as file:
    for line in file:
        row = list(map(float, line.strip().split()))
        if row:
            data.append(row)

num_inputs = len(data[0]) - 1
epochs = int(input("Enter number of epochs: "))
weights = [float(input(f"Enter initial w{i+1}: ")) for i in range(num_inputs)]
b = float(input("Enter initial bias (b): "))
alpha = float(input("Enter learning rate (alpha): "))
theta = float(input("Enter threshold (theta): "))

def activation(yin):
    if yin > theta: return 1
    elif yin < -theta: return -1
    return 0

# Header and Separator for consistent styling
headers = f"{'Inputs (x)':<12} | {'t':<2} | {'yin':>6} | {'y':>2} | {'Status':<10}"
separator = "-" * len(headers)

for epoch in range(epochs):
    print(f"\n{'='*15} EPOCH {epoch+1} {'='*15}")
    print(headers)
    print(separator)

    converged = True
    for row in data:
        x_elements = row[:-1]
        t = int(row[-1])
        yin = b + sum(x * w for x, w in zip(x_elements, weights))
        y = activation(yin)

        if y != t:
            converged = False
            for i in range(num_inputs):
                weights[i] += alpha * t * x_elements[i]
            b += alpha * t
            status = "UPDATED"
        else:
            status = "OK"

        x_str = " ".join([f"{int(x):>2}" for x in x_elements])
        print(f"{x_str:<12} | {t:>2} | {yin:>6.2f} | {y:>2} | {status}")

    # Updated values displayed below the table
    w_vals = "  ".join([f"w{i+1}={w:.2f}" for i, w in enumerate(weights)])
    print(f"\n>> UPDATED PARAMETERS (Epoch {epoch+1}):")
    print(f"   Weights: [{w_vals}]")
    print(f"   Bias:    {b:.2f}")

    if converged:
        print(f"\n[!] STOPPING: Convergence reached (y = t for all rows).")
        break

print(f"\n{'*'*40}\n   TRAINING COMPLETE\n{'*'*40}")
