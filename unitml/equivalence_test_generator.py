# UnitML
# Copyright 2023 Carnegie Mellon University.
# NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN "AS-IS" BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.
# Released under a BSD (SEI)-style license, please see license.txt or contact permission@sei.cmu.edu for full terms.
# [DISTRIBUTION STATEMENT A] This material has been approved for public release and unlimited distribution.  Please see Copyright notice for non-US Government use and distribution.
# This Software includes and/or makes use of Third-Party Software each subject to its own license.
# DM23-0976


from string import Template

from unitml.helpers import *


equivalence_test_template = Template(
    "\t@pytest.mark.parametrize(\"equivalence_value\", ${equivalence_list})\n"
    "\tdef test_equivalence_${item_index}_${test_index}(self, equivalence_value):\n"
    "\t\ttest_input = DataPipelineInput()\n"
    "\t\tprint(\"This is an equivalence test for ${item}\")\n"
    "\t\tprint(\"The value being passed is \" + ${value_format} + \" which is ${expected_result} the classes\")\n"
    "${additional_setup}"
    "\t\ttest_input.input${item_index} = equivalence_value\n"
    "\t\tdata_pipeline_output = data_pipeline_instance.run(${input_string})\n"
    "\t\tmodel_output = model_instance.run(data_pipeline_output)\n"
    "${assert}"
)


def generate_integer_equivalence_tests(test_file, item, item_index, input_string, additional_setup_str, success_assert_string, failure_assert_string):
    test_file.write(f"\t# Testing the equivalence classes of {item['item_name']}\n")
    test_file.write(f"\t# Tests outside classes\n")
    test_file.write(equivalence_test_template.substitute(
        {
            "equivalence_list": f"["
                "None"
            "]",
            "item": item['item_name'],
            "item_index": item_index,
            "test_index": 1,
            "input_string": input_string,
            "value_format": "str(equivalence_value)",
            "additional_setup" : additional_setup_str,
            "expected_result": "outside",
            "assert": failure_assert_string
        }
    ))


def generate_float_equivalence_tests(test_file, item, item_index, input_string, additional_setup_str, success_assert_string, failure_assert_string):
    test_file.write(f"\t# Testing the equivalence classes of {item['item_name']}\n")
    test_file.write(f"\t# Tests outside classes\n")
    test_file.write(equivalence_test_template.substitute(
        {
            "equivalence_list": f"["
                "None"
            "]",
            "item": item['item_name'],
            "item_index": item_index,
            "test_index": 1,
            "input_string": input_string,
            "value_format": "str(equivalence_value)",
            "additional_setup" : additional_setup_str,
            "expected_result": "outside",
            "assert": failure_assert_string
        }
    ))


def generate_string_equivalence_tests(test_file, item, item_index, input_string, additional_setup_str, success_assert_string, failure_assert_string):
    success_cases = "["
    failure_cases = "[None, "

    if item['item_specification']['empty']:
        success_cases += "\"\", "
    else:
        failure_cases += "\"\" ,"

    numeric_str = generate_numeric_string(item['item_specification']["min_length"], item['item_specification']["max_length"])
    if item['item_specification']["numeric"]:
        success_cases += "\"" + numeric_str + "\", "
    else:
        failure_cases += "\"" + numeric_str + "\", "

    slashes_str = generate_slashes_string(item['item_specification']["min_length"], item['item_specification']["max_length"])
    if item['item_specification']["slashes"]:
        success_cases += "\"" + slashes_str + "\", "
    else:
        failure_cases += "\"" + slashes_str + "\", "

    spaces_str = generate_spaces_str(item['item_specification']["min_length"], item['item_specification']["max_length"])
    if item['item_specification']["spaces"]:
        success_cases += "\"" + spaces_str + "\", "
    else:
        failure_cases += "\"" + spaces_str + "\", "

    special_str = generate_special_string(item['item_specification']["min_length"], item['item_specification']["max_length"])
    if item['item_specification']["special"]:
        success_cases += "\"" + special_str + "\", "
    else:
        failure_cases += "\"" + special_str + "\", "

    if len(success_cases) > 1:
        success_cases = success_cases[:-2]
    success_cases += "]"

    if len(failure_cases) > 1:
        failure_cases = failure_cases[:-2]
    failure_cases += "]"

    test_file.write(f"\t# Testing the equivalence classes of {item['item_name']}\n")
    test_file.write(f"\t# Tests inside classes\n")
    test_file.write(equivalence_test_template.substitute(
        {
            "equivalence_list": success_cases,
            "item": item['item_name'],
            "item_index": item_index,
            "test_index": 0,
            "input_string": input_string,
            "value_format": "str(equivalence_value)",
            "additional_setup" : additional_setup_str,
            "expected_result": "inside",
            "assert": success_assert_string
        }
    ))

    test_file.write(f"\t# Tests outside classes\n")
    test_file.write(equivalence_test_template.substitute(
        {
            "equivalence_list": failure_cases,
            "item": item['item_name'],
            "item_index": item_index,
            "test_index": 1,
            "input_string": input_string,
            "value_format": "str(equivalence_value)",
            "additional_setup" : additional_setup_str,
            "expected_result": "outside",
            "assert": failure_assert_string
        }
    ))


def generate_image_equivalence_tests(test_file, item, item_index, input_string, additional_setup_str, success_assert_string, failure_assert_string):
    test_file.write(f"\t# Testing the equivalence classes of {item['item_name']}\n")
    test_file.write("\t# Tests inside classes\n")

    channels = item["item_specification"]["channels"]
    correct_mode = "L" if channels == 1 else "RGB"
    incorrect_mode = "RGB" if channels == 1 else "L"

    test_file.write(equivalence_test_template.substitute(
        {
            "equivalence_list": f"["
                f"Image.new(\"{correct_mode}\", size=({item['item_specification']['resolution_x']}, {item['item_specification']['resolution_y']}))"
            "]",
            "item": item['item_name'],
            "item_index": item_index, 
            "test_index": 0,
            "input_string": input_string,
            "value_format": f"\"an image with correct number of channels\"",
            "additional_setup" : additional_setup_str,
            "expected_result": "inside",
            "assert": success_assert_string
        }
    ))

    test_file.write(f"\t# Tests outside classes\n")
    test_file.write(equivalence_test_template.substitute(
        {
            "equivalence_list": f"["
                f"Image.new(\"{incorrect_mode}\", size=({item['item_specification']['resolution_x']}, {item['item_specification']['resolution_y']})), "
            "]",
            "item": item['item_name'],
            "item_index": item_index, 
            "test_index": 1,
            "input_string": input_string,
            "value_format": f"\"an image incorrect number of channels\"",
            "additional_setup" : additional_setup_str,
            "expected_result": "outside",
            "assert": failure_assert_string
        }
    ))