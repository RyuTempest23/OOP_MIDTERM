import json
from pathlib import Path
from abc import ABC, abstractmethod


# Abstraction: using abc module
class Employee(ABC):
    def __init__(self, name, age, gender, position, salary):
        self.__name = name
        self.__age = age
        self.__gender = gender
        self.__position = position
        self.__salary = salary

    # Encapsulation: using getters/setters
    def get_name(self): return self.__name
    def set_name(self, value): self.__name = value.strip().title()

    def get_age(self): return self.__age
    def set_age(self, value):
        if isinstance(value, int) and value > 0:
            self.__age = value
        else:
            print("Invalid age!")

    def get_gender(self): return self.__gender
    def set_gender(self, value): self.__gender = value.strip().title()

    def get_position(self): return self.__position
    def set_position(self, value): self.__position = value.strip().title()

    def get_salary(self): return self.__salary
    def set_salary(self, value):
        if isinstance(value, (int, float)) and value > 0:
            self.__salary = value
        else:
            print("Salary must be positive!")

    @abstractmethod
    def display_info(self): pass


# Inheritance: inherits from Employee class
class PartTimeEmployee(Employee):
    def __init__(self, name, age, gender, position, salary, hourly_rate, hours_worked):
        super().__init__(name, age, gender, position, salary)
        self.__hourly_rate = hourly_rate
        self.__hours_worked = hours_worked

    def get_hourly_rate(self): return self.__hourly_rate
    def set_hourly_rate(self, value):
        if value > 0:
            self.__hourly_rate = value
        else:
            print("Hourly rate must be positive!")

    def get_hours_worked(self): return self.__hours_worked
    def set_hours_worked(self, value):
        if value >= 0:
            self.__hours_worked = value
        else:
            print("Hours worked must be non-negative!")

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


class FullTimeEmployee(Employee):
    def __init__(self, name, age, gender, position, salary, monthly_bonus_pay):
        super().__init__(name, age, gender, position, salary)
        self.__monthly_bonus_pay = monthly_bonus_pay

    def get_monthly_bonus_pay(self): return self.__monthly_bonus_pay
    def set_monthly_bonus_pay(self, value):
        if value >= 0:
            self.__monthly_bonus_pay = value
        else:
            print("Monthly bonus must be non-negative!")

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


# Main System class to handle CRUD operations
class EmployeeManagementSystem:
    def __init__(self):
        self.path = Path("employees.json")
        self.employees = {
            "Part-Time Employees": {},
            "Full-Time Employees": {}
        }
        self.part_id = 1
        self.full_id = 1
        self.running = True
        self.load_data()

    # Utility Functions
    def valid_integer(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input! Please enter a number.")

    def valid_float(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input! Please enter a number.")

    def load_data(self):
        if self.path.exists():
            try:
                with open(self.path, "r") as f:
                    self.employees = json.load(f)
            except json.JSONDecodeError:
                print("Warning: employees.json is empty or corrupted. Starting fresh.")

    def save_data(self):
        with open(self.path, "w") as f:
            json.dump(self.employees, f, indent=4)

    def get_employee_type_key(self, choice):
        return "Part-Time Employees" if choice == 1 else "Full-Time Employees"

    def display_records(self, emp_type_key):
        emp_dict = self.employees.get(emp_type_key, {})
        if not emp_dict:
            print(f"No {emp_type_key} records found.")
            return
        for emp_id, emp_data in emp_dict.items():
            print(f"\nID: {emp_id}")
            for k, v in emp_data.items():
                print(f"  {k}: {v}")

    # CRUD Operations
    def add_employee(self):
        print("\n1. Part-Time Employee\n2. Full-Time Employee")
        choice = self.valid_integer("Enter employee type: ")

        if choice not in (1, 2):
            print("Invalid type!")
            return

        name = input("Enter Name: ").strip().title()
        age = self.valid_integer("Enter Age: ")
        gender = input("Enter Gender: ").strip().title()
        position = input("Enter Position: ").strip().title()
        salary = self.valid_float("Enter Salary: ")

        emp_type_key = self.get_employee_type_key(choice)

        if choice == 1:
            hourly_rate = self.valid_float("Enter Hourly Rate: ")
            hours_worked = self.valid_integer("Enter Hours Worked: ")
            emp = PartTimeEmployee(name, age, gender, position, salary, hourly_rate, hours_worked)
            emp_id = str(self.part_id)
            self.part_id += 1
        else:
            bonus = self.valid_float("Enter Monthly Bonus Pay: ")
            emp = FullTimeEmployee(name, age, gender, position, salary, bonus)
            emp_id = str(self.full_id)
            self.full_id += 1

        self.employees[emp_type_key][emp_id] = emp.display_info()
        self.save_data()
        print("Employee added successfully!")

    def view_employee(self):
        print("\n1. All Employees\n2. Part-Time\n3. Full-Time")
        choice = self.valid_integer("Choose view option: ")

        match choice:
            case 1:
                print("\n=== All Employees ===")
                for emp_type in self.employees:
                    self.display_records(emp_type)
            case 2:
                print("\n=== Part-Time Employees ===")
                self.display_records("Part-Time Employees")
            case 3:
                print("\n=== Full-Time Employees ===")
                self.display_records("Full-Time Employees")
            case _:
                print("Invalid choice!")

    def search_employee(self):
        keyword = input("Enter name or position to search: ").strip().lower()
        found = False
        for emp_type, emp_dict in self.employees.items():
            for emp_id, emp_data in emp_dict.items():
                if keyword in emp_data["Name"].lower() or keyword in emp_data["Position"].lower():
                    print(f"\n[{emp_type}] ID: {emp_id}")
                    for k, v in emp_data.items():
                        print(f"  {k}: {v}")
                    found = True
        if not found:
            print("No matching employee found.")

    def update_employee(self):
        print("\n1. Part-Time Employee\n2. Full-Time Employee")
        choice = self.valid_integer("Enter employee type: ")
        emp_type_key = self.get_employee_type_key(choice)

        if emp_type_key not in self.employees or not self.employees[emp_type_key]:
            print(f"No {emp_type_key} data found.")
            return

        self.display_records(emp_type_key)
        emp_id = input("Enter Employee ID to update: ").strip()

        if emp_id not in self.employees[emp_type_key]:
            print("Employee ID not found.")
            return

        emp_data = self.employees[emp_type_key][emp_id]
        print("Leave field blank to skip update.")

        for field in list(emp_data.keys())[1:]:  # skip Type
            new_value = input(f"Enter new {field} (current: {emp_data[field]}): ").strip()
            if new_value:
                emp_data[field] = float(new_value) if field in ("Salary", "Hourly Rate", "Monthly Bonus Pay") else new_value.title()

        self.save_data()
        print("Employee updated successfully!")

    def delete_employee(self):
        print("\n1. Delete File\n2. Delete All Data\n3. Delete Individual")
        choice = self.valid_integer("Enter choice: ")

        if choice == 1:
            if self.path.exists():
                self.path.unlink()
                self.employees = {"Part-Time Employees": {}, "Full-Time Employees": {}}
                print("File deleted.")
            else:
                print("No JSON file found.")
        elif choice == 2:
            self.employees = {"Part-Time Employees": {}, "Full-Time Employees": {}}
            self.save_data()
            print("All employee data cleared.")
        elif choice == 3:
            print("\n1. Part-Time\n2. Full-Time")
            emp_choice = self.valid_integer("Choose type: ")
            emp_type_key = self.get_employee_type_key(emp_choice)
            if not self.employees[emp_type_key]:
                print("No records to delete.")
                return
            self.display_records(emp_type_key)
            emp_id = input("Enter Employee ID to delete: ").strip()
            if emp_id in self.employees[emp_type_key]:
                del self.employees[emp_type_key][emp_id]
                self.save_data()
                print("Employee deleted.")
            else:
                print("Employee ID not found.")
        else:
            print("Invalid choice!")

    def exit_program(self):
        print("Thank you for using my system... Goodbye!")
        self.running = False

    def menu(self):
        while self.running:
            print("\n===== EMPLOYEE MANAGEMENT SYSTEM =====")
            print("1. Add Employee")
            print("2. View Employees")
            print("3. Search Employee")
            print("4. Update Employee")
            print("5. Delete Employee")
            print("6. Exit")

            choice = self.valid_integer("Enter choice: ")
            match choice:
                case 1: self.add_employee()
                case 2: self.view_employee()
                case 3: self.search_employee()
                case 4: self.update_employee()
                case 5: self.delete_employee()
                case 6: self.exit_program()
                case _: print("Invalid choice!")


# Main program entry
if __name__ == "__main__":
    EmployeeManagementSystem().menu()