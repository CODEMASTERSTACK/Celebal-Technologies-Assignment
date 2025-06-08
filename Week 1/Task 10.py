# Formatting strings with the format() method
print("{:<15} {:>5}".format("Name", 25))
print("{:^15} {:^5}".format("Name", 25))      

# Formatting numbers, including padding with zeros
print("{:0>5}".format(42))   

# Formatting floats with commas and fixed precision
print("{:,.2f}".format(1234567.8910))  # Output: 1,234,567.89

# Example of a table-like output
header = "{:<10} {:>8} {:^12}"
row = "{:<10} {:>8.2f} {:^12}"
print(header.format("Item", "Price", "Quantity"))
print(row.format("Apple", 1.59, 10))
print(row.format("Banana", 0.79, 25))


name = "kripal"
age = 20
balance = 453424.54

# Basic f-string formatting with alignment
print(f"{name:<10} {age:>5}")  

# Formatting numbers with padding and precision inside f-strings
print(f"{balance:0>12.2f}")

# Creating a neat table output with f-strings
print(f"{'Item':<10} {'Price':>10} {'Quantity':^10}")
print(f"{'Laptop':<10} {432312.91:>10.2f} {5:^10}")
print(f"{'Phone':<10} {9000.00:>10.2f} {15:^10}")

# Aligning strings and numbers using the % operator
print("%-10s %5d" % ("Kripal", 20))

# Formatting a float
print("%08.2f" % (45.678))
