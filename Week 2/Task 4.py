import string

def print_rangoli():
    size = int(input("Enter size: "))
    alpha = string.ascii_lowercase[:size]
    for i in range(size-1, -size, -1):
        print('-'.join(alpha[size-1:abs(i):-1] + alpha[abs(i):size]).center(size*4-3, '-'))

print_rangoli()
