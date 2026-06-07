#Grade Calculator

print("__GRADE EVALUATION SYSTEM__")
marks=float(input("Enter your marks(0-100):"))    #taking inpput
if marks >=90:
 grade="A+"
 comment="Exclelent Performance!"
elif marks>=70:
 grade="A"
 comment="Grate Job!"
elif marks>=60:
 grade="B+"
 comment="Good,  Keep it up and make it bigger"
elif marks>=50:
 grade="B"
 comment="Satisfactory!"
elif marks>=40:
 grade="B-"
 comment="Bad Result, DO WORK HARD!"
elif 0<=marks<40:
 grade="F"
 comment="Failed, don't give up!"
else:
 grade="Invalid"
 comment="Please enter marks between 0 and 100"
print(f"\nGrade:{grade}")

print(f"Teacher's Remark:{commment}")


