my_set = {10, 20, 30, 40, 50}

#Using Discard(): Remove element if exist
my_set.discard(30)  
my_set.discard(100)  


#Using Remove(): Remove element but make error if not present.
try:
    my_set.remove(40)  
    my_set.remove(100) 
except KeyError:
    print("Error: Element not found in set!")

popped_element = my_set.pop()
print("Popped element:", popped_element)

print("Updated set:", my_set)
