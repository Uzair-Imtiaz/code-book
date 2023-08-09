""" Contains a utility function to calculate the age of the user """

from datetime import date


def calculate_age(birth_date):
    """ Calculates and returns the age of a user """

    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age
