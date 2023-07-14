import math


def generate_numeric_string(min_length, max_length):
    str = "123test123"
    return string_length_adjust(str, min_length, max_length)


def generate_slashes_string(min_length, max_length):
    str = "/\test\/"
    return string_length_adjust(str, min_length, max_length)


def generate_special_string(min_length, max_length):
    str = "@t#$test^&t*"
    return string_length_adjust(str, min_length, max_length)


def generate_spaces_str(min_length, max_length):
    str = " test test "
    return string_length_adjust(str, min_length, max_length)


def string_length_adjust(str, min_length, max_length):
    """
    Adjusts the inputted string to the a length between the min and max length.
    Pass the same value for min and max to get a specific length.
    """
    str_length = max_length - int(((max_length - min_length) / 2))
    str = str * math.ceil((max_length / len(str)))
    str = str[:str_length]
    return str