from collections import Counter

def total_earnings(inventory, sales):
    stock = Counter(inventory)  
    return sum(price for size, price in sales if stock[size] and not stock.subtract([size]))

inventory = [42, 41, 42, 44, 42, 40, 41]  
sales = [(42, 500), (41, 600), (40, 450), (44, 700), (42, 500)]  

print("Total earnings:", total_earnings(inventory, sales))
