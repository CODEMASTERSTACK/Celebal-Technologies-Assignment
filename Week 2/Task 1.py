words = "Celebal Technologies enhances operational efficiency through advanced data analytics and AI solutions"

#Method 1: Using Ttle Function
print(words.title())

#Method 2: Creating Own Function

def cap_word(text):
     return ' '.join(word.capitalize() for word in text.split())


capital_word_output = cap_word(words)
print(capital_word_output)
