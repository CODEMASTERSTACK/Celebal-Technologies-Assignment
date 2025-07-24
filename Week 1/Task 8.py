my_tuple = (1, 2, 3, "apple")
print("Original tuple:", my_tuple)

#Accessing elements
print("First element:", my_tuple[0])
print("Slice of tuple:", my_tuple[1:3])

#Attempting to modify the tuple
try:
    my_tuple[1] = 100
except TypeError as error:
    print("Error when trying to modify tuple:", error)

# Using a tuple as a key in a dictionary because tuples are immutable
dictionary = {}
key = (1, 2, 3)  
dictionary[key] = "This tuple is used as a key"
print("Dictionary with tuple key:", dictionary)

# Checking the hash of a tuple
print("Hash of key (1, 2, 3):", hash(key))

#If a tuple contains a mutable object like a list then it is not hashable
mutable_tuple = (1, 2, [3, 4])
try:
    print("Hash of mutable_tuple:", hash(mutable_tuple))
except TypeError as error:
    print("Cannot hash mutable_tuple because it contains a mutable element:", error)
