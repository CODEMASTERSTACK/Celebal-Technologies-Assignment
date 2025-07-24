def divide_numbers(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero!"
    except TypeError:
        return "Error : Please enter numeric values!"
    else:
        return f"Result: {result:.2f}"
    finally:
        print("Execution completed.")

#Simple Case
print(divide_numbers(10, 2))

#Dividing by Zero
print(divide_numbers(10, 0))

#Invalid Input
print(divide_numbers(10, "a"))
