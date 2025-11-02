from abc import ABC, abstractmethod


# Abstraction class
class Person(ABC):
    """Represent a person's information"""

    def __init__(self, name, age, gender, contact):
        """Initialize person's private attributes"""
        self.__name    = name
        self.__age     = age
        self.__gender  = gender
        self.__contact = contact

    # Encapsulation: getters and setters
    def get_name(self):
        return self.__name
    
    def set_name(self, new_name):
        if new_name == "":
            print("Name must not be empty.")
        else:
            self.__name = new_name
    
    def get_age(self):
        return self.__age
    
    def set_age(self, new_age):
        if isinstance(new_age, int):
            if new_age < 0:
                print("Age cannot be negative.")
            else:
                self.__age = new_age
        else:
            print("Invalid input.")

    def get_gender(self):
        return self.__gender
    
    def set_gender(self, new_gender):
        if new_gender == "":
            print("Gender must not be empty.")
        else:
            self.__gender = new_gender

    def get_contact(self):
        return self.__contact
    
    def set_contact(self, new_contact):
        if new_contact == "":
            print("Contact must not be empty.")
        else:
            if not new_contact.isdigit():
                print("Please enter digit value.")
            else:
                self.__contact = new_contact
    
    @abstractmethod
    def display_info(self):
        pass


# Inheritance: inherits from Abstract class
class Patient(Person):
    """Represent patient's record"""

    def __init__(self, name, age, gender, contact, patient_id, address):
        super().__init__(name, age, gender, contact)
        """Initialize patient's private attributes"""

        self.__patient_id = patient_id
        self.__address    = address
    
    # Encapsulation: getters and setters
    def get_patient_id(self):
        return self.__patient_id
    
    def set_patient_id(self, new_id):
        if isinstance(new_id, int):
            if new_id < 1:
                print("Patient ID must be greater than zero.")
            else:
                self.__patient_id = new_id
        else:
            print("Invalid input.")

    def get_address(self):
        return self.__address
    
    def set_address(self, new_address):
        if new_address == "":
            print("Address must not be empty.")
        else:
            self.__address = new_address

    # Polymorphism: override display_info() from class Person(grandparent class)
    def display_info(self):
        """Displays the patient's information"""
        print(f"ID: {self.__patient_id}")
        print(f"Name: {self.__name}")
        print(f"Age: {self.__age}")
        print(f"Gender: {self.__gender}")
        print(f"Contact: {self.__contact}")
        print(f"Address: {self.__address}")


class InPatient(Patient):
    """Represents In-Patient's record"""

    def __init__(self, name, age, gender, contact, patient_id, address, room_number, admission_date, discharge_date):
        super().__init__(name, age, gender, contact, patient_id, address)
        """Initialize In-Patient's private attributes"""

        self.__room_number = room_number
        self.__admission_date = admission_date
        self.__discharge_date = discharge_date

    # Encapsulation: getters and setters
    def get_room_number(self):
        return self.__room_number
    
    def set_room_number(self, new_room_number):
        if isinstance(new_room_number, int):
            if new_room_number < 0:
                print("Negative room number is not allowed.")
            else:
                self.__room_number = new_room_number
        else:
            print("Invalid room number.")

    def get_admission_date(self):
        return self.__admission_date
    
    def set_admission_date(self, new_admission_date):
        if new_admission_date == "":
            print("Admission date cannot be empty.")
        else:
            self.__admission_date = new_admission_date

    def get_discharge_date(self):
        return self.__discharge_date
    
    def set_discharge_date(self, new_discharge_date):
        if new_discharge_date == "":
            print("Discharge date cannot be empty.")
        else:
            self.__discharge_date = new_discharge_date

    # Polymorphism: override display_info() from class Patient(parent class)
    def display_info(self):
        """Displays the In-Patient's information"""
        print(f"Type: In-Patient")
        super().display_info()
        print(f"Room Number: {self.__room_number}")
        print(f"Admission Date: {self.__admission_date}")
        print(f"Discharge Date: {self.__discharge_date}")


class OutPatient(Patient):
    """Represents Out-Patient's record"""

    def __init__(self, name, age, gender, contact, patient_id, address, attending_physician, visit_date):
        super().__init__(name, age, gender, contact, patient_id, address)
        """Initialize Out-Patient's private attributes"""
        
        self.__attending_physician = attending_physician
        self.__visit_date = visit_date

    # Encapsulation: getters and setters
    def get_attending_physician(self):
        return self.__attending_physician
    
    def set_attending_physician(self, new_attending_physician):
        if new_attending_physician == "":
            print("Attending physician must require a name.")
        else:
            self.__attending_physician = new_attending_physician

    def get_visit_date(self):
        return self.__visit_date
    
    def set_visit_date(self, new_visit_date):
        if new_visit_date == "":
            print("Visit date cannot be empty.")
        else:
            self.__visit_date = new_visit_date

    # Polymorphism: override display_info() from class Patient(parent class)
    def display_info(self):
        """Displays the Out-Patient's information"""
        print("Type: Out-Patient")
        super().display_info()
        print(f"Attending Physician: {self.__attending_physician}")
        print(f"Visit Date: {self.__visit_date}")


class Program:
    """Patient Record System's Main Class"""

    def __init__(self):
        self.patients = []

    def add_patient(self):
        """Add patient's info"""
        print("===== Add Patient =====\n")
        patient_type = input("Choose a patient type (in-patient or out-patient): ").strip().lower()

        if patient_type != "in-patient" or patient_type != "out-patient":
            print("Please choose only between in-patient or out-patient.")
            return

        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        gender = input("Enter Gender: ")
        contact = input("Enter Contact: ")
        patient_id = int(input("Input ID: "))
        address = input("Enter Address: ")
        
        if patient_type == "in-patient":
            room_number = int(input("Enter Room Number: "))
            admission_date = input("Enter Admission Date: ")
            discharge_date = input("Enter Discharge Date: ")
            patient = InPatient(name, age, gender, contact, 
                                patient_id, address, room_number, 
                                admission_date, discharge_date)
        elif patient_type == "out-patient":
           attending_physician = input("Input attending physician: ")
           visit_date = input("Input visit date: ")
           patient = OutPatient(name, age, gender, 
                                contact, patient_id, address, 
                                attending_physician, visit_date)

        self.patients.append(patient)
        print("Patient added successfully!")

    def view_patient(self):
        """View patient's record"""
        print("===== View Patient Record =====\n")

        if not self.patients:
            print("No records found.")
            return
        
        for patient in self.patients:
            patient.display_info()
            print("===========================")
    
    def update_patient(self):
        """Modify patien's record"""
        print("===== Update Patient =====\n")

        p_id = int(input("Enter Patient ID to update: "))
        for patient in self.patients:
            if patient.get_patient_id() == p_id:
                pass