import itertools

def calculate_probability():
    n = int(input("Enter the total number of letters: "))
    letters = input("Enter the letters separated by spaces: ").split()
    k = int(input("Enter the number of letters to select: "))
    all_combos = itertools.combinations(letters, k)

    total_combos = 0       
    combos_with_a = 0
    
    for combo in all_combos:
        total_combos += 1
        if 'a' in combo:
            combos_with_a += 1
    probability = combos_with_a / total_combos if total_combos else 0
    print("Probability that at least one 'a' is selected: {:.3f}".format(probability))

calculate_probability()
