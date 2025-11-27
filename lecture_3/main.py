"""
Student Grade Analyzer

Interactive program to manage students and their grades.
"""

from typing import List, Optional, Tuple, TypedDict


class Student(TypedDict):
    name: str
    grades: List[int]


Students = List[Student]


MENU = (
    "\nStudent Grade Analyzer\n"
    "1. Add a new student\n"
    "2. Add grades for a student\n"
    "3. Show report (all students)\n"
    "4. Find top performer\n"
    "5. Exit\n"
)


def create_student(name: str) -> Student:
    """Create a student dictionary given a name."""
    return {"name": name, "grades": []}


def find_student(students: Students, name: str) -> Optional[Student]:
    """
    Find a student by  name.
    Returns the student dict or None if not found.
    """
    name_lower = name.strip().lower()
    for student in students:
        if student.get("name", "").strip().lower() == name_lower:
            return student
    return None


def add_student(students: Students, name: str) -> bool:
    """
    Add a new student if not present.
    Returns True if added, False if already exists.
    """
    if find_student(students, name) is not None:
        return False
    students.append(create_student(name.strip()))
    return True


def add_grades_to_student(students: Students, name: str) -> Tuple[bool, str]:
    """
    Interactively add grades to the student with the given name.
    Valid grades are integers in [0, 100].
    Returns (True, message) if student found,
    otherwise (False, error_message).
    """
    student = find_student(students, name)
    if student is None:
        return False, f"Student '{name}' does not exist."

    added_count = 0
    # Interactive loop for entering grades
    while True:
        raw = input("Enter a grade (or 'done' to finish): ").strip()
        if raw.lower() == "done":
            break
        try:
            grade = int(raw)
            if 0 <= grade <= 100:
                student["grades"].append(grade)
                added_count += 1
            else:
                print("Grade must be an integer between 0 "
                      "and 100 inclusive.")
        except ValueError:
            print("Invalid input. Please enter an integer grade or 'done'.")

    return True, f"Added {added_count} grade(s) for {student['name']!s}."


def average(grades: List[int]) -> Optional[float]:
    """
    Compute average of grades list.
    Returns None if the list is empty.
    """
    if not grades:
        return None
    return sum(grades) / len(grades)


def show_report(students: Students) -> None:
    """
    Print a report for all students:
    - Each student's average (or N/A)
    - Summary: max, min, overall average (consider only students with grades)
    """
    if not students:
        print("No students in the system.")
        return

    averages: List[float] = []
    print("\n--- Student Report ---")
    for s in students:
        name = s.get("name", "Unknown")
        grades = s.get("grades", [])
        avg = average(grades)

        if avg is None:
            print(f"{name}'s average grade is N/A (no grades).")
        else:
            print(f"{name}'s average grade is {avg:.2f}.")
            averages.append(avg)

    # Summary statistics
    if not averages:
        print("\nNo grades available for summary (no student has grades).")
    else:
        max_avg = max(averages)
        min_avg = min(averages)
        overall_avg = sum(averages) / len(averages)
        print("\nSummary:")
        print(f"Max Average: {max_avg:.2f}")
        print(f"Min Average: {min_avg:.2f}")
        print(f"Overall Average: {overall_avg:.2f}")


def find_top_performer(students: Students) -> None:
    """
    Find and print the top performer by average grade.
    Students with no grades are ignored.
    """
    best: Optional[Tuple[Student, float]] = None  # (student, average)
    for s in students:
        avg = average(s["grades"])
        if avg is None:
            continue
        if best is None or avg > best[1]:
            best = (s, avg)

    if best is None:
        print("No top performer: no grades recorded.")
    else:
        student, grade = best
        print(
            f"The student with the highest average is {student['name']} "
            f"with a grade of {grade:.2f}."
        )


def read_choice(prompt: str = "Enter your choice: ") -> Optional[int]:
    """
    Read a menu choice and return it as an integer.
    Returns None if input is invalid.
    """
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        return None


def main_loop() -> None:
    """
    The interactive main loop (menu).
    Keeps running until the user chooses to Exit.
    """
    students: Students = []  # starting data store
    while True:
        print(MENU)
        try:
            choice = read_choice()
            if choice is None:
                print("Invalid input. Please type a number from 1 to 5.")
                continue

            if choice == 1:
                name = input("Enter student name: ").strip()
                if not name:
                    print("Empty name. Aborted.")
                    continue
                added = add_student(students, name)
                if not added:
                    print(f"Student '{name}' already exists.")
                else:
                    print(f"Student '{name}' added.")

            elif choice == 2:
                name = input("Enter student name: ").strip()
                if not name:
                    print("Empty name. Aborted.")
                    continue
                ok, message = add_grades_to_student(students, name)
                print(message)

            elif choice == 3:
                show_report(students)

            elif choice == 4:
                find_top_performer(students)

            elif choice == 5:
                print("Exiting program.")
                break

            else:
                print("Please choose a number from 1 to 5.")

        except KeyboardInterrupt:
            # Friendly handling of Ctrl+C
            print("\nInterrupted by user. Exiting.")
            break
        except Exception as exc:
            # Catch-all to avoid crash; in production you'd log the error
            print(f"An unexpected error occurred: {exc}")
            break


if __name__ == "__main__":
    main_loop()
