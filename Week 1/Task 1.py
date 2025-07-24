score_value = input("Enter the student's score from (0-100): ")

try:
    score = float(score_value)
    
    if score < 0 or score > 100:
        print("Invalid score. Please enter a number between 0 and 100.")
    
    elif score >= 90:
        print("Grade A")
    elif score >= 80:
        print("Grade B")
    elif score >= 70:
        print("Grade C")
    elif score >= 60:
        print("Grade D")
    elif score >=34:
        print("Grade E")
    else:
        print("Grade F")
        
except ValueError:
    print("Invalid input. Please enter a numeric value.")
