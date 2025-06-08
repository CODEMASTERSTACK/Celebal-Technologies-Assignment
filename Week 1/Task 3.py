import itertools

def compress_string(string):
    
    parts=[]
    for char, group in itertools.groupby(string):
        count = len(list(group))
        parts.append(f"{count}{char}")
    return " ".join(parts)


string = input("Enter the string for compressing: ")
compressed_string = compress_string(string)
print(compressed_string)
