import math

from string import Template


equivalence_test_template = Template(
    "\t@pytest.mark.parametrize(\"equivalence_value\", ${equivalence_list})\n"
    "\tdef test_equivalence_${item_index}_${test_index}(self, equivalence_value):\n"
    "\t\ttest_input = DataPipelineInput()\n"
    "\t\ttest_input.input${item_index} = equivalence_value\n"
    "\t\tdata_pipeline_output = data_pipeline_instance.run(${input_string})\n"
    "\t\tmodel_output = model_instance.run(data_pipeline_output)\n"
    "${assert}"
)


def generate_integer_equivalence_tests(test_file, item, item_index, input_string, success_assert_string, failure_assert_string):
    test_file.write(f"\t# Testing the equivalence classes of {item['item_name']}\n")
    test_file.write("\t# Tests outside classes that are expected to fail\n")
    test_file.write("\t@pytest.mark.xfail\n")
    test_file.write(equivalence_test_template.substitute(
        {
            "equivalence_list": f"["
                "None"
            "]",
            "item_index": item_index,
            "test_index": 1,
            "input_string": input_string,
            "assert": failure_assert_string
        }
    ))


def generate_float_equivalence_tests():
    pass


def generate_string_equivalence_tests(test_file, item, item_index, input_string, success_assert_string, failure_assert_string):
    success_cases = "["
    failure_cases = "[None, "

    special_str = generate_special_string(item["min_length"], item["max_length"])
    if item["special"]:
        success_cases += "\"" + special_str + "\", "
    else:
        failure_cases += "\"" + special_str + "\", "

    spaces_str = generate_spaces_str(item["min_length"], item["max_length"])
    if item["spaces"]:
        success_cases += "\"" + spaces_str + "\", "
    else:
        failure_cases += "\"" + spaces_str + "\", "

    if item['empty']:
        success_cases += "\"\", "
    else:
        failure_cases += "\"\" ,"

    if len(success_cases) > 1:
        success_cases = success_cases[:-2]
    success_cases += "]"

    if len(failure_cases) > 1:
        failure_cases = failure_cases[:-2]
    failure_cases += "]"

    test_file.write(f"\t# Testing the equivalence classes of {item['item_name']}\n")
    test_file.write("\t# Valid tests\n")
    test_file.write(equivalence_test_template.substitute(
        {
            "equivalence_list": success_cases,
            "item_index": item_index,
            "test_index": 0,
            "input_string": input_string,
            "assert": success_assert_string
        }
    ))

    test_file.write("\t# Tests outside classes that are expected to fail\n")
    test_file.write("\t@pytest.mark.xfail\n")
    test_file.write(equivalence_test_template.substitute(
        {
            "equivalence_list": failure_cases,
            "item_index": item_index,
            "test_index": 1,
            "input_string": input_string,
            "assert": failure_assert_string
        }
    ))


def generate_image_equivalence_tests():
    pass


def generate_special_string(min_length, max_length):
    str = "@t#$test^&t*"
    return string_length_adjust(str, min_length, max_length)


def generate_spaces_str(min_length, max_length):
    str = " test test "
    return string_length_adjust(str, min_length, max_length)


def string_length_adjust(str, min_length, max_length):
    str_length = max_length - int(((max_length - min_length) / 2))
    str = str * math.ceil((max_length / len(str)))
    str = str[:str_length]
    return str