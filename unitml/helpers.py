# UnitML
# Copyright 2023 Carnegie Mellon University.
# NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN "AS-IS" BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.
# Released under a BSD (SEI)-style license, please see license.txt or contact permission@sei.cmu.edu for full terms.
# [DISTRIBUTION STATEMENT A] This material has been approved for public release and unlimited distribution.  Please see Copyright notice for non-US Government use and distribution.
# This Software includes and/or makes use of Third-Party Software each subject to its own license.
# DM23-0976


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