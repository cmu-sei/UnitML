# UnitML
# Copyright 2023 Carnegie Mellon University.
# NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN "AS-IS" BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.
# Released under a BSD (SEI)-style license, please see license.txt or contact permission@sei.cmu.edu for full terms.
# [DISTRIBUTION STATEMENT A] This material has been approved for public release and unlimited distribution.  Please see Copyright notice for non-US Government use and distribution.
# This Software includes and/or makes use of Third-Party Software each subject to its own license.
# DM23-0976


import string, random

from string import Template

from unitml.helpers import string_length_adjust


boundary_test_template = Template(
    "\t@pytest.mark.parametrize(\"boundary_value\", ${boundary_list})\n"
    "\tdef test_boundary_${item_index}_${test_index}(self, boundary_value):\n"
    "\t\tprint(\"This is a boundary test for ${item}\")\n"
    "\t\tprint(\"The value being passed is \" + ${value_format} + \" which is ${expected_result} the boundaries\")\n"
    "${additional_setup}"
    "\t\ttest_input = DataPipelineInput()\n"
    "\t\ttest_input.input${item_index} = boundary_value\n"
    "\t\tdata_pipeline_output = data_pipeline_instance.run(${input_string})\n"
    "\t\tmodel_output = model_instance.run(data_pipeline_output)\n"
    "${assert}"
)


def generate_integer_boundary_tests(test_file, item, item_index, input_string, additional_setup_str, success_assert_string, failure_assert_string):
    test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")
    test_file.write(f"\t# Tests inside boundaries\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"{item['item_specification']['min_value']}, "
                f"{item['item_specification']['min_value'] + 1}, "
                f"{item['item_specification']['max_value'] - 1}, "
                f"{item['item_specification']['max_value']}"
            "]",
            "item": item['item_name'],
            "item_index": item_index,
            "test_index": 0,
            "input_string": input_string,
            "value_format": "str(boundary_value)",
            "additional_setup" : additional_setup_str,
            "expected_result": "inside",
            "assert": success_assert_string,
        }
    ))

    test_file.write(f"\t# Tests outside boundaries\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"{item['item_specification']['min_value'] - 1}, "
                f"{item['item_specification']['max_value'] + 1}"
            "]",
            "item": item['item_name'],
            "item_index": item_index,
            "test_index": 1,
            "input_string": input_string,
            "value_format": "str(boundary_value)",
            "additional_setup" : additional_setup_str,
            "expected_result": "outside",
            "assert": failure_assert_string
        }
    ))


def generate_float_boundary_tests(test_file, item, item_index, input_string, additional_setup_str, success_assert_string, failure_assert_string):
    test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")
    test_file.write(f"\t# Test inside boundaries\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"{item['item_specification']['min_value']:.2f}, "
                f"{item['item_specification']['min_value'] + .01:.2f}, "
                f"{item['item_specification']['max_value'] - .01:.2f}, "
                f"{item['item_specification']['max_value']:.2f}"
            "]",
            "item": item['item_name'],
            "item_index": item_index,
            "test_index": 0,
            "input_string": input_string,
            "value_format": "str(boundary_value)",
            "additional_setup" : additional_setup_str,
            "expected_result": "inside",
            "assert": success_assert_string
        }
    ))

    test_file.write(f"\t# Tests outside boundaries\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"{item['item_specification']['min_value'] - .01:.2f}, "
                f"{item['item_specification']['max_value'] + .01:.2f}"
            "]",
            "item": item['item_name'],
            "item_index": item_index,
            "test_index": 1,
            "input_string": input_string,
            "value_format": "str(boundary_value)",
            "additional_setup" : additional_setup_str,
            "expected_result": "outside",
            "assert": failure_assert_string
        }
    ))


def generate_string_boundary_tests(test_file, item, item_index, input_string, additional_setup_str, success_assert_string, failure_assert_string):
    test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")
    test_file.write(f"\t# Tests inside boundaries\n")
    str = string_length_adjust("Test", item['item_specification']["max_length"] + 1, item['item_specification']["max_length"] + 1)
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"\"{str[:item['item_specification']['min_length']]}\", "
                f"\"{str[:item['item_specification']['min_length'] + 1]}\", "
                f"\"{str[:item['item_specification']['max_length'] - 1]}\", "
                f"\"{str[:item['item_specification']['max_length']]}\""
            "]",
            "item": item['item_name'],
            "item_index": item_index, 
            "test_index": 0,
            "input_string": input_string,
            "value_format": "str(boundary_value)",
            "additional_setup" : additional_setup_str,
            "expected_result": "inside",
            "assert": success_assert_string
        }
    ))

    test_file.write(f"\t# Tests outside boundaries\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"\"{str[:item['item_specification']['min_length'] - 1]}\", "
                f"\"{str[:item['item_specification']['max_length'] + 1]}\""
            "]",
            "item": item['item_name'],
            "item_index": item_index, 
            "test_index": 1,
            "input_string": input_string,
            "value_format": "str(boundary_value)",
            "additional_setup" : additional_setup_str,
            "expected_result": "outside",
            "assert": failure_assert_string
        }
    ))


def generate_image_boundary_tests(test_file, item, item_index, input_string, additional_setup_str, success_assert_string, failure_assert_string):
    test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")
    test_file.write("\t# Tests inside boundaries\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"Image.new(\"RGB\", size=({item['item_specification']['resolution_x']}, {item['item_specification']['resolution_y']}))"
            "]",
            "item": item['item_name'],
            "item_index": item_index, 
            "test_index": 0,
            "input_string": input_string,
            "value_format": "\"an image of resulution \" + str(boundary_value.size)",
            "additional_setup" : additional_setup_str,
            "expected_result": "inside",
            "assert": success_assert_string
        }
    ))

    test_file.write(f"\t# Tests outside boundaries\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"Image.new(\"RGB\", size=({item['item_specification']['resolution_x'] - 1}, {item['item_specification']['resolution_y'] - 1})), "
                f"Image.new(\"RGB\", size=({item['item_specification']['resolution_x'] + 1}, {item['item_specification']['resolution_y'] + 1}))"
            "]",
            "item": item['item_name'],
            "item_index": item_index, 
            "test_index": 1,
            "input_string": input_string,
            "value_format": "\"an image of resulution \" + str(boundary_value.size)",
            "additional_setup" : additional_setup_str,
            "expected_result": "outside",
            "assert": failure_assert_string
        }
    ))