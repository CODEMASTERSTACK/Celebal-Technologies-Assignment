import textwrap

def wrap_text(text, width):
    return textwrap.fill(text, width)

text = "Celebal Technologies enhances operational efficiency through advanced data analytics and AI solutions"
wrapped_text = wrap_text(text, 15)
print(wrapped_text)
