import inspect
import re
import unittest
import math

# Define below the class 'Circle' and it's methods with proper doctests.
class Circle:

    def __init__(self, radius):
        # Define the initialization method below
        try:
            if not isinstance(radius, (int, float)):
                raise TypeError
            elif 1000 >=radius>=0:
                    self.radius=radius
            else:
                raise ValueError
        except ValueError:
            raise ValueError("radius must be between 0 and 1000 inclusive")
        except TypeError:
            raise TypeError("radius must be a number")

    def area(self):
        # Define the area functionality below
        y=math.pi*(self.radius**2)
        return round(y,2)

    def circumference(self):
        # Define the circumference functionality below
        x=math.pi*2*self.radius
        return round(x,2)