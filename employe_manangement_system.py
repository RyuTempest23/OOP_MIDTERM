from abc import ABC, abstractmethod


# Abstraction: using abc module
class Employee(ABC):
    def __init__(self, name, age, gender, position, salary):
        # Private attributes
        self.__name = name
        self.__age = age
        self.__gender = gender
        self.__position = position
        self.__salary = salary

    # Encapsulation: using getters/setters
    def get_name(self):
        return self.__name

    def set_name(self, new_name):
        self.__name = new_name

    def get_age(self):
        return self.__age

    def set_age(self, new_age):
        if isinstance(new_age, int) and new_age > 0:
            self.__age = new_age
        else:
            print("Invalid age!")

    def get_gender(self):
        return self.__gender

    def set_gender(self, new_gender):
        self.__gender = new_gender

    def get_position(self):
        return self.__position

    def set_position(self, new_position):
        self.__position = new_position

    def get_salary(self):
        return self.__salary

    def set_salary(self, amount):
        if isinstance(amount, float) and amount > 0:
            self.__salary = amount
        else:
            print("Salary cannot be negative!")

    # ===== Abstract Method =====
    @abstractmethod
    def display_info(self):
        pass


# Inheritance: inherits from parent class (Employee)
class PartTimeEmployee(Employee):
    def __init__(self, name, age, gender, position, salary, hourly_rate, hours_worked):
        super().__init__(name, age, gender, position, salary)
        self.__hourly_rate = hourly_rate
        self.__hours_worked = hours_worked

    def get_hourly_rate(self):
        return self.__hourly_rate

    def set_hourly_rate(self, rate):
        if isinstance(rate, float) and rate > 0:
            self.__hourly_rate = rate
        else:
            print("Hourly rate cannot be negative!")

    def get_hours_worked(self):
        return self.__hours_worked

    def set_hours_worked(self, hours):
        if isinstance(hours, int) and hours > 0:
            self.__hours_worked = hours
        else:
            print("Hours worked cannot be negative!")

    # Polymorphism: overriding the display_info() method from parent class
    def display_info(self):
        return {
            "Type": "Part-Time",
            "Name": self.get_name(),
            "Age": self.get_age(),
            "Gender": self.get_gender(),
            "Position": self.get_position(),
            "Salary": self.get_salary(),
            "Hourly Rate": self.get_hourly_rate(),
            "Hours Worked": self.get_hours_worked()
        }


class FullTimeEmployee(Employee):
    def __init__(self, name, age, gender, position, salary, monthly_bonus_pay):
        super().__init__(name, age, gender, position, salary)
        self.__monthly_bonus_pay = monthly_bonus_pay

    def get_monthly_bonus_pay(self):
        return self.__monthly_bonus_pay

    def set_monthly_bonus_pay(self, bonus_pay):
        if isinstance(bonus_pay, float) and bonus_pay > 0:
            self.__monthly_bonus_pay = bonus_pay
        else:
            print("Monthly bonus pay cannot be negative!")

    def display_info(self):
        return {
            "Type": "Full-Time",
            "Name": self.get_name(),
            "Age": self.get_age(),
            "Gender": self.get_gender(),
            "Position": self.get_position(),
            "Salary": self.get_salary(),
            "Monthly Bonus Pay": self.get_monthly_bonus_pay()
        }

class EmployeeManagementSystem:
    def __init__(self):
        self.employees = {
            "Part-Time Employees": {},
            "Full-Time Employees": {}
        }
        self.part_time_id_counter = 1
        self.full_time_id_counter = 1
        self.not_done = True

    # Input Validation: get valid input for integer and float data type
    def valid_integer(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a number.")

    def valid_float(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a number.")

    # ===== Add Employee =====
    def add_employee(self):
        while True:
            print("\n===== Add Employee =====\n")
            print("1. Part-Time Employee")
            print("2. Full-Time Employee")
            print("3. Back to Main Menu")

            choice = self.valid_integer("\nChoose a number: ")

            if choice not in (1, 2, 3):
                print("\nPlease select only between 1–3.")
                continue

            if choice == 3:
                print("\nReturning to main menu...")
                break

            name = input("\nEnter Name: ").strip().title()
            age = self.valid_integer("Enter Age: ")
            gender = input("Enter Gender: ").strip().title()
            position = input("Enter Position: ").strip().title()
            salary = self.valid_float("Enter Salary: ")

            if choice == 1:
                hourly_rate = self.valid_float("Enter Hourly Rate: ")
                hours_worked = self.valid_integer("Enter Hours Worked: ")
                employee = PartTimeEmployee(name, age, gender, position, salary, hourly_rate, hours_worked)
                emp_id = self.part_time_id_counter
                self.employees["Part-Time Employees"][emp_id] = employee
                self.part_time_id_counter += 1
            else:
                monthly_bonus = self.valid_float("Enter Monthly Bonus Pay: ")
                employee = FullTimeEmployee(name, age, gender, position, salary, monthly_bonus)
                emp_id = self.full_time_id_counter
                self.employees["Full-Time Employees"][emp_id] = employee
                self.full_time_id_counter += 1

            print("\nEmployee added successfully!")

    # ===== View Employee =====
    def view_employee(self):
        while True:
            print("\n===== View Employees =====\n")
            print("1. View All Employees")
            print("2. View Part-Time Employees")
            print("3. View Full-Time Employees")
            print("4. Back to Main Menu")

            choice = self.valid_integer("\nChoose a number: ")

            match choice:
                case 1:
                    print("\n===== All Employees =====")
                    has_data = False
                    for category, records in self.employees.items():
                        print(f"\n--- {category} ---")
                        if not records:
                            print("No records found.")
                        else:
                            has_data = True
                            for emp_id, emp in records.items():
                                print(f"ID: {emp_id}:")
                                for key, value in emp.display_info().items():
                                    print(f"    {key}: {value}")
                    if not has_data:
                        print("\nNo employees found at all.")
                case 2:
                    self._display_records("Part-Time Employees", "Part-Time")
                case 3:
                    self._display_records("Full-Time Employees", "Full-Time")
                case 4:
                    print("\nReturning to main menu...")
                    break
                case _:
                    print("Invalid choice! Please select between 1–4.")

    # Helper method for viewing employee records
    def _display_records(self, category, label):
        print(f"\n===== {label} Employees =====")
        records = self.employees[category]
        if not records:
            print(f"No {label.lower()} employees found.")
        else:
            for emp_id, emp in records.items():
                print(f"ID: {emp_id}:")
                for key, value in emp.display_info().items():
                    print(f"    {key}: {value}")

    # ===== Update Employee =====
    def update_employee(self):
        while True:
            print("\n===== Update Employee =====\n")
            print("1. Part-Time Employee")
            print("2. Full-Time Employee")
            print("3. Back to Main Menu")

            choice = self.valid_integer("\nChoose a number: ")

            if choice not in (1, 2, 3):
                print("Please select only between 1–3.")
                return

            if choice == 3:
                print("\nReturning to main menu...")
                break

            emp_type = "Part-Time Employees" if choice == 1 else "Full-Time Employees"
            emp_id = self.valid_integer("Enter Employee ID: ")

            if emp_id not in self.employees[emp_type]:
                print("Employee ID not found.")
                return

            emp = self.employees[emp_type][emp_id]

            print("\nLeave blank to keep the current value.\n")

            # Common fields
            new_name = input(f"New Name ({emp.get_name()}): ").strip().title() or emp.get_name()
            new_age = input(f"New Age ({emp.get_age()}): ").strip() or emp.get_age()
            new_gender = input(f"New Gender ({emp.get_gender()}): ").strip().title() or emp.get_gender()
            new_position = input(f"New Position ({emp.get_position()}): ").strip().title() or emp.get_position()
            new_salary = input(f"New Salary ({emp.get_salary()}): ").strip() or emp.get_salary()

            # Apply updates safely
            emp.set_name(new_name)
            if str(new_age).isdigit():
                emp.set_age(int(new_age))
            emp.set_gender(new_gender)
            emp.set_position(new_position)
            try:
                emp.set_salary(float(new_salary))
            except ValueError:
                print("Invalid salary input, keeping old value.")

            # Type-specific fields
            if emp_type == "Part-Time Employees":
                new_rate = input(f"New Hourly Rate ({emp.get_hourly_rate()}): ").strip() or emp.get_hourly_rate()
                new_hours = input(f"New Hours Worked ({emp.get_hours_worked()}): ").strip() or emp.get_hours_worked()
                if str(new_rate).replace('.', '', 1).isdigit():
                    emp.set_hourly_rate(float(new_rate))
                if str(new_hours).isdigit():
                    emp.set_hours_worked(int(new_hours))
            else:
                new_bonus = input(f"New Monthly Bonus ({emp.get_monthly_bonus_pay()}): ").strip() or emp.get_monthly_bonus_pay()
                if str(new_bonus).replace('.', '', 1).isdigit():
                    emp.set_monthly_bonus_pay(float(new_bonus))

            print("\nEmployee updated successfully!\n")

    # ===== Delete Employee =====
    def delete_employee(self):
        while True:
            print("\n===== Delete Employee =====\n")
            print("1. Delete All Employee Records")
            print("2. Delete All Part-Time Employees")
            print("3. Delete All Full-Time Employees")
            print("4. Delete Employee by ID")
            print("5. Back to Main Menu")

            choice = self.valid_integer("\nChoose a number: ")

            match choice:
                case 1:
                    self.employees["Part-Time Employees"].clear()
                    self.employees["Full-Time Employees"].clear()
                    print("\nAll employees deleted.")
                case 2:
                    self.employees["Part-Time Employees"].clear()
                    print("\nAll part-time employees deleted.")
                case 3:
                    self.employees["Full-Time Employees"].clear()
                    print("\nAll full-time employees deleted.")
                case 4:
                    self._delete_by_id()
                case 5:
                    print("\nReturning to main menu...")
                    break
                case _:
                    print("\nInvalid choice! Please select between 1–5.")

    # Helper method for deleting employee record by ID
    def _delete_by_id(self):
        print("\n===== Delete By ID =====\n")
        emp_type_choice = self.valid_integer("1. Part-Time\n2. Full-Time\n\nChoose: ")
        emp_type = "Part-Time Employees" if emp_type_choice == 1 else "Full-Time Employees"
        emp_id = self.valid_integer("\nEnter Employee ID: ")

        if emp_id in self.employees[emp_type]:
            del self.employees[emp_type][emp_id]
            print("\nEmployee deleted.")
        else:
            print("\nEmployee not found.")

    # ===== Exit =====
    def exit_program(self):
        print("\nThank you for using my system. Goodbye!")
        self.not_done = False

    # ===== Menu =====
    def menu(self):
        while self.not_done:
            print("\n===== Employee Management System =====\n")
            print("1. Add Employee")
            print("2. View Employee")
            print("3. Update Employee")
            print("4. Delete Employee")
            print("5. Exit")

            choice = self.valid_integer("\nChoose a number of your choice based on the menu: ")

            match choice:
                case 1: self.add_employee()
                case 2: self.view_employee()
                case 3: self.update_employee()
                case 4: self.delete_employee()
                case 5: self.exit_program()
                case _: print("Invalid choice! Please try again.")


# Main program entry
if __name__ == "__main__":
    main = EmployeeManagementSystem()
    main.menu()
