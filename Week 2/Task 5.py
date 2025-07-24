def split_and_deduplicate(text, part_size):
    return ["".join(dict.fromkeys(text[i:i+part_size])) for i in range(0, len(text), part_size)]

text = "kkkrrippaallll"
part_size = 5
result = split_and_deduplicate(text, part_size)
print(result)
