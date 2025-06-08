n = int(input("Enter the number of students: "))
student_marks = {}
    
for _ in range(n):
    data = input("Enter student name followed by their marks separated by space: ").split()
    name = data[0]
    marks = list(map(float, data[1:]))  
    student_marks[name] = marks
    query_name = input("Enter the student's name to find the average marks: ")
    
    marks_list = student_marks.get(query_name, [])
    if marks_list:
        average = sum(marks_list) / len(marks_list)
        print(f"{average:.2f}")
    else:
        print("Student not found.")
