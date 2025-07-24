def minion_game(s):
    vowels = "aeiou"
    kripal = 0
    naitik = 0
    n = len(s)

    for i in range(n):
        score = n-i
        if s[i] in vowels:
            kripal += score
        else:
            naitik += score

    if kripal > naitik:
        print("Kripal: ", kripal)
    elif naitik > kripal:
        print("Naitik", naitik)
    else:
        print("Draw")

s = input("Enter the string: ").lower()
minion_game(s)
