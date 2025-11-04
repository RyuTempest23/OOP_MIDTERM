import json, os
from pathlib import Path
from abc import ABC, abstractmethod


# Abstract Class (Abstraction)
class Employee(ABC):
    def __init__(self, name, age, gender, position, salary):
        # Private attributes (Encapsulation)
        self.__name = name
        self.__age = age
        self.__gender = gender
        self.__position = position
        self.__salary = salary

    # Getters and Setters
    def get_name(self): return self.__name
    def set_name(self, value): self.__name = value.strip().title()

    def get_age(self): return self.__age
    def set_age(self, value):
        if isinstance(value, int) and value > 0:
            self.__age = value
        else:
            print("\n\t[!] Invalid age input.")

    def get_gender(self): return self.__gender
    def set_gender(self, value): self.__gender = value.strip().title()

    def get_position(self): return self.__position
    def set_position(self, value): self.__position = value.strip().title()

    def get_salary(self): return self.__salary
    def set_salary(self, value):
        if isinstance(value, (int, float)) and value > 0:
            self.__salary = value
        else:
            print("\n\t[!] Salary must be positive!")

    # Abstract method (must be implemented by subclasses)
    @abstractmethod
    def display_info(self):
        pass


# Part-Time Employee (Inheritance)
class PartTimeEmployee(Employee):
    def __init__(self, name, age, gender, position, salary, hourly_rate, hours_worked):
        super().__init__(name, age, gender, position, salary)
        self.__hourly_rate = hourly_rate
        self.__hours_worked = hours_worked

    # Overriding display_info() (Polymorphism)
    def display_info(self):
        return {
            "Type": "Part-Time",
            "Name": self.get_name(),
            "Age": self.get_age(),
            "Gender": self.get_gender(),
            "Position": self.get_position(),
            "Salary": self.get_salary(),
            "Hourly Rate": self.__hourly_rate,
            "Hours Worked": self.__hours_worked
        }


# Full-Time Employee (Inheritance)
class FullTimeEmployee(Employee):
    def __init__(self, name, age, gender, position, salary, monthly_bonus_pay):
        super().__init__(name, age, gender, position, salary)
        self.__monthly_bonus_pay = monthly_bonus_pay

    def display_info(self):
        return {
            "Type": "Full-Time",
            "Name": self.get_name(),
            "Age": self.get_age(),
            "Gender": self.get_gender(),
            "Position": self.get_position(),
            "Salary": self.get_salary(),
            "Monthly Bonus Pay": self.__monthly_bonus_pay
        }


# Main System Class
class EmployeeManagementSystem:
    def __init__(self):
        self.path = Path("employees.json")
        self.employees = {"Part-Time Employees": {}, "Full-Time Employees": {}}
        self.part_id = 1
        self.full_id = 1
        self.running = True
        self.load_data()

    # For Decoration
    def decorate(self, text):
        print("\n" + "=" * 45)
        print("\t" + text)
        print("=" * 45)

    # Input Validators
    def valid_integer(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("\n\t[!] Please enter a valid integer.")

    def valid_float(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("\n\t[!] Please enter a valid number.")

    # File Handling
    def load_data(self):
        if self.path.exists():
            with open(self.path, "r") as f:
                self.employees = json.load(f)

            # Update part-time and full-time IDs based on existing data
            part_ids = self.employees["Part-Time Employees"].keys()
            full_ids = self.employees["Full-Time Employees"].keys()

            if part_ids:
                self.part_id = max(map(int, part_ids)) + 1
            if full_ids:
                self.full_id = max(map(int, full_ids)) + 1
        else:
            self.save_data()


    def save_data(self):
        with open(self.path, "w") as f:
            json.dump(self.employees, f, indent=4)

    def get_employee_type_key(self, choice):
        return "Part-Time Employees" if choice == 1 else "Full-Time Employees"

    def display_records(self, emp_type_key):
        emp_dict = self.employees.get(emp_type_key, {})
        if not emp_dict:
            print(f"\n\tNo {emp_type_key} records found.")
            return
        print(f"\n\t=== {emp_type_key} ===")
        for emp_id, emp_data in emp_dict.items():
            print(f"\n\tEmployee ID: {emp_id}")
            for k, v in emp_data.items():
                print(f"\t  {k}: {v}")

    # CRUD Operations
    def add_employee(self):
        while True:
            self.decorate("ADD EMPLOYEE")
            print("\t1. Part-Time")
            print("\t2. Full-Time")
            print("\t3. Back to Main Menu")
            choice = self.valid_integer("\n\tEnter choice: ")

            match choice:
                case 1 | 2:
                    print("\n\t--- Employee Details ---")
                    name = input("\tEnter Name: ").strip().title()
                    age = self.valid_integer("\tEnter Age: ")
                    gender = input("\tEnter Gender: ").strip().title()
                    position = input("\tEnter Position: ").strip().title()
                    salary = self.valid_float("\tEnter Salary: ")
                    emp_type_key = self.get_employee_type_key(choice)

                    if choice == 1:
                        hourly_rate = self.valid_float("\tEnter Hourly Rate: ")
                        hours_worked = self.valid_integer("\tEnter Hours Worked: ")
                        emp = PartTimeEmployee(name, age, gender, position, salary, hourly_rate, hours_worked)
                        emp_id = str(self.part_id)
                        self.part_id += 1
                    else:
                        bonus = self.valid_float("\tEnter Monthly Bonus Pay: ")
                        emp = FullTimeEmployee(name, age, gender, position, salary, bonus)
                        emp_id = str(self.full_id)
                        self.full_id += 1

                    self.employees[emp_type_key][emp_id] = emp.display_info()
                    self.save_data()
                    print("\n\tEmployee added successfully!")

                case 3:
                    break
                case _:
                    print("\n\t[!] Invalid choice.")

    def view_employee(self):
        while True:
            self.decorate("VIEW EMPLOYEE")
            print("\t1. All Employees")
            print("\t2. Part-Time")
            print("\t3. Full-Time")
            print("\t4. Back to Main Menu")
            choice = self.valid_integer("\n\tEnter choice: ")

            match choice:
                case 1:
                    for emp_type in self.employees:
                        self.display_records(emp_type)
                case 2:
                    self.display_records("Part-Time Employees")
                case 3:
                    self.display_records("Full-Time Employees")
                case 4:
                    break
                case _:
                    print("\n\t[!] Invalid choice.")

    def search_employee(self):
        while True:
            self.decorate("SEARCH EMPLOYEE")
            print("\t1. Start Search")
            print("\t2. Back to Main Menu")
            choice = self.valid_integer("\n\tEnter choice: ")

            match choice:
                case 1:
                    keyword = input("\tEnter name or position: ").strip().lower()
                    found = False
                    for emp_type, emp_dict in self.employees.items():
                        for emp_id, emp_data in emp_dict.items():
                            if keyword in emp_data["Name"].lower() or keyword in emp_data["Position"].lower():
                                print(f"\n\t[{emp_type}] ID: {emp_id}")
                                for k, v in emp_data.items():
                                    print(f"\t  {k}: {v}")
                                found = True
                    if not found:
                        print("\n\t[!] No matching employee found.")
                case 2:
                    break
                case _:
                    print("\n\t[!] Invalid choice.")

    def update_employee(self):
        while True:
            self.decorate("UPDATE EMPLOYEE")
            print("\t1. Start Update")
            print("\t2. Back to Main Menu")
            choice = self.valid_integer("\n\tEnter choice: ")

            match choice:
                case 1:
                    print("\n\t--- Choose Employee Type ---")
                    print("\t1. Part-Time")
                    print("\t2. Full-Time")
                    emp_choice = self.valid_integer("\n\tEnter type: ")
                    emp_type_key = self.get_employee_type_key(emp_choice)

                    if not self.employees[emp_type_key]:
                        print(f"\n\tNo {emp_type_key} data found.")
                        continue

                    self.display_records(emp_type_key)
                    emp_id = input("\n\tEnter Employee ID to update: ").strip()

                    if emp_id not in self.employees[emp_type_key]:
                        print("\n\t[!] Employee ID not found.")
                        continue

                    emp_data = self.employees[emp_type_key][emp_id]
                    print("\n\tLeave blank to skip a field.")

                    for field in list(emp_data.keys())[1:]:
                        new_value = input(f"\tNew {field} (current: {emp_data[field]}): ").strip()
                        if new_value:
                            emp_data[field] = float(new_value) if field in ("Salary", "Hourly Rate", "Monthly Bonus Pay") else new_value.title()

                    self.save_data()
                    print("\n\tEmployee updated successfully!")
                case 2:
                    break
                case _:
                    print("\n\t[!] Invalid choice.")

    def delete_employee(self):
        while True:
            self.decorate("DELETE EMPLOYEE")
            print("\t1. Delete File")
            print("\t2. Delete All Data")
            print("\t3. Delete Individual Record")
            print("\t4. Back to Main Menu")
            choice = self.valid_integer("\n\tEnter choice: ")

            match choice:
                case 1:
                    if self.path.exists():
                        self.path.unlink()
                        self.employees = {"Part-Time Employees": {}, "Full-Time Employees": {}}
                        print("\n\tFile deleted successfully.")
                    else:
                        print("\n\t[!] No JSON file found.")
                case 2:
                    self.employees = {"Part-Time Employees": {}, "Full-Time Employees": {}}
                    self.save_data()
                    print("\n\tAll employee data cleared.")
                case 3:
                    print("\n\t--- Choose Employee Type ---")
                    print("\t1. Part-Time")
                    print("\t2. Full-Time")
                    emp_choice = self.valid_integer("\n\tEnter type: ")
                    emp_type_key = self.get_employee_type_key(emp_choice)

                    if not self.employees[emp_type_key]:
                        print("\n\tNo records found.")
                        continue

                    self.display_records(emp_type_key)
                    emp_id = input("\n\tEnter Employee ID to delete: ").strip()
                    if emp_id in self.employees[emp_type_key]:
                        del self.employees[emp_type_key][emp_id]
                        self.save_data()
                        print("\n\tEmployee deleted successfully.")
                    else:
                        print("\n\t[!] Employee ID not found.")
                case 4:
                    break
                case _:
                    print("\n\t[!] Invalid choice.")

    def exit_program(self):
        print("\n" + "=" * 55)
        print("\tThank you for using the system! Goodbye.")
        print("=" * 55)
        self.running = False

    def menu(self):
        while self.running:
            self.decorate("EMPLOYEE MANAGEMENT SYSTEM")
            print("\t1. Add Employee")
            print("\t2. View Employees")
            print("\t3. Search Employee")
            print("\t4. Update Employee")
            print("\t5. Delete Employee")
            print("\t6. Exit")

            choice = self.valid_integer("\n\tEnter choice: ")

            match choice:
                case 1: self.add_employee()
                case 2: self.view_employee()
                case 3: self.search_employee()
                case 4: self.update_employee()
                case 5: self.delete_employee()
                case 6: self.exit_program()
                case _: print("\n\t[!] Invalid choice.")


# Entry Point
if __name__ == "__main__":
    EmployeeManagementSystem().menu()