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

    if item['empty']:
        success_cases += "\"\", "
    else:
        failure_cases += "\"\" ,"

    numeric_str = generate_numeric_string(item["min_length"], item["max_length"])
    if item["numeric"]:
        success_cases += "\"" + numeric_str + "\", "
    else:
        failure_cases += "\"" + numeric_str + "\", "

    slashes_str = generate_slashes_string(item["min_length"], item["max_length"])
    if item["slashes"]:
        success_cases += "\"" + slashes_str + "\", "
    else:
        failure_cases += "\"" + slashes_str + "\", "

    spaces_str = generate_spaces_str(item["min_length"], item["max_length"])
    if item["spaces"]:
        success_cases += "\"" + spaces_str + "\", "
    else:
        failure_cases += "\"" + spaces_str + "\", "

    special_str = generate_special_string(item["min_length"], item["max_length"])
    if item["special"]:
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