def set_avg(numbers):
    return sum(numbers) / len(numbers) if numbers else 0

number_set = {20,43,55,34,12,33,432}
average = set_avg(number_set)
print(f"The average is: {average:.2f}")
