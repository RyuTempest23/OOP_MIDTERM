from abc import ABC, abstractmethod

# Abstraction
class Person(ABC):
    """Represent a person's identity"""

    def __init__(self, name, age):
        """Initialize person's attributes"""
        self.__name = name
        self.__age  = age

    # Encapsulation: getters and setters method
    def get_name(self):
        return self.__name
    
    def set_name(self, new_name):
        self.__name = new_name

    def get_age(self):
        return self.__age
    
    def set_age(self, new_age):
        if isinstance(new_age, int) > 0:
            self.__age = new_age
        else:
            print("Invalid age!")

    @abstractmethod
    def display_info(self):
        pass


