import pandas as pd

# Function to display current hypotheses at each step
def show(specific_h, general_h, step):
    print(f"\n--- Step {step} ---")
    print("Specific Hypothesis (S):", specific_h)
    print("General Hypothesis (G):")
    for h in general_h:
        print(h)

# Candidate Elimination Algorithm
def candidate_elimination(concepts, target):
    # Step 1: Initialize the Specific Hypothesis with the first example
    specific_h = concepts[0].copy()

    # Step 2: Initialize the General Hypothesis with the most general values
    general_h = []
    for i in range(len(specific_h)):
        row = []
        for j in range(len(specific_h)):
            row.append('?')
        general_h.append(row)

    # Show initial hypotheses
    show(specific_h, general_h, 0)

    # Step 3: Process each training example
    for i in range(len(concepts)):
        example = concepts[i]
        label = target[i].lower()

        if label == 'yes':
            # Positive example: Generalize the specific hypothesis
            for j in range(len(specific_h)):
                if specific_h[j] != example[j]:
                    specific_h[j] = '?'

            # Remove inconsistent hypotheses from general_h
            updated_general_h = []
            for h in general_h:
                consistent = True
                for k in range(len(h)):
                    if h[k] != '?' and h[k] != specific_h[k]:
                        consistent = False
                        break
                if consistent:
                    updated_general_h.append(h)
            general_h = updated_general_h

        else:
            # Negative example: Specialize the general hypotheses
            new_general_h = []
            for h in general_h:
                for j in range(len(specific_h)):
                    if specific_h[j] != '?' and specific_h[j] != example[j]:
                        new_h = h.copy()
                        new_h[j] = specific_h[j]
                        if new_h not in new_general_h:
                            new_general_h.append(new_h)
            general_h = new_general_h

        # Show current hypotheses
        show(specific_h, general_h, i + 1)

    # Step 4: Remove overly general hypotheses (like all '?')
    final_general_h = []
    for g in general_h:
        has_specific = False
        for attr in g:
            if attr != '?':
                has_specific = True
                break
        if has_specific:
            final_general_h.append(g)

    return specific_h, final_general_h

# Step 5: Load the dataset
data = pd.read_csv("play_tennis.csv")

# Step 6: Split into concepts (input) and target (output)
concepts = data.iloc[:, :-1].values.tolist()
target = data.iloc[:, -1].values.tolist()

# Step 7: Run the algorithm
final_s, final_g = candidate_elimination(concepts, target)

# Step 8: Display final result
print("\nFinal Specific Hypothesis:", final_s)
print("Final General Hypotheses:")
for g in final_g:
    print(g)
