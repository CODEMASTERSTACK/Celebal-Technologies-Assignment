from collections import OrderedDict

def word_order(sentence):
    words = sentence.split()
    counts = OrderedDict()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    
    return counts

sentence = input("Enter a sentence: ")
result = word_order(sentence)

for word, count in result.items():
    print(word, count)
