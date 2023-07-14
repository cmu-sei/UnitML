import string, random

from string import Template

from model_test.helpers import string_length_adjust


boundary_test_template = Template(
    "\t@pytest.mark.parametrize(\"boundary_value\", ${boundary_list})\n"
    "\tdef test_boundary_${item_index}_${test_index}(self, boundary_value):\n"
    "\t\ttest_input = DataPipelineInput()\n"
    "\t\ttest_input.input${item_index} = boundary_value\n"
    "\t\tdata_pipeline_output = data_pipeline_instance.run(${input_string})\n"
    "\t\tmodel_output = model_instance.run(data_pipeline_output)\n"
    "${assert}"
)


def generate_integer_boundary_tests(test_file, item, item_index, input_string, success_assert_string, failure_assert_string):
    test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")
    test_file.write("\t# Valid Tests\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"{item['min_value']}, "
                f"{item['min_value'] + 1}, "
                f"{item['max_value'] - 1}, "
                f"{item['max_value']}"
            "]",
            "item_index": item_index,
            "test_index": 0,
            "input_string": input_string,
            "assert": success_assert_string,
        }
    ))

    test_file.write("\t# Tests outside boundaries that are expected to fail\n")
    test_file.write("\t@pytest.mark.xfail\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"{item['min_value'] - 1}, "
                f"{item['max_value'] + 1}"
            "]",
            "item_index": item_index,
            "test_index": 1,
            "input_string": input_string,
            "assert": failure_assert_string
        }
    ))


def generate_float_boundary_tests(test_file, item, item_index, input_string, success_assert_string, failure_assert_string):
    test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")
    test_file.write("\t# Valid Tests\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"{item['min_value']:.2f}, "
                f"{item['min_value'] + .01:.2f}, "
                f"{item['max_value'] - .01:.2f}, "
                f"{item['max_value']:.2f}"
            "]",
            "item_index": item_index,
            "test_index": 0,
            "input_string": input_string,
            "assert": success_assert_string
        }
    ))

    test_file.write("\t# Tests outside boundaries that are expected to fail\n")
    test_file.write("\t@pytest.mark.xfail\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"{item['min_value'] - .01:.2f}, "
                f"{item['max_value'] + .01:.2f}"
            "]",
            "item_index": item_index,
            "test_index": 1,
            "input_string": input_string,
            "assert": failure_assert_string
        }
    ))


def generate_string_boundary_tests(test_file, item, item_index, input_string, success_assert_string, failure_assert_string):
    test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")
    test_file.write("\t# Valid Tests\n")
    str = string_length_adjust("Test", item["max_length"] + 1, item["max_length"] + 1)
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"\"{str[:item['min_length']]}\", "
                f"\"{str[:item['min_length'] + 1]}\", "
                f"\"{str[:item['max_length'] - 1]}\", "
                f"\"{str[:item['max_length']]}\""
            "]",
            "item_index": item_index, 
            "test_index": 0,
            "input_string": input_string,
            "assert": success_assert_string
        }
    ))

    test_file.write("\t# Tests outside boundaries that are expected to fail\n")
    test_file.write("\t@pytest.mark.xfail\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"\"{str[:item['min_length'] - 1]}\", "
                f"\"{str[:item['max_length'] + 1]}\""
            "]",
            "item_index": item_index, 
            "test_index": 1,
            "input_string": input_string,
            "assert": failure_assert_string
        }
    ))


def generate_image_boundary_tests(test_file, item, item_index, input_string, success_assert_string, failure_assert_string):
    test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")
    test_file.write("\t# Valid Tests\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"Image.new(\"RGB\", size=({item['resolution_x']}, {item['resolution_y']}))"
            "]",
            "item_index": item_index, 
            "test_index": 0,
            "input_string": input_string,
            "assert": success_assert_string
        }
    ))

    test_file.write("\t# Tests outside boundaries that are expected to fail\n")
    test_file.write("\t@pytest.mark.xfail\n")
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"Image.new(\"RGB\", size=({item['resolution_x'] - 1}, {item['resolution_y'] - 1})), "
                f"Image.new(\"RGB\", size=({item['resolution_x'] + 1}, {item['resolution_y'] + 1}))"
            "]",
            "item_index": item_index, 
            "test_index": 1,
            "input_string": input_string,
            "assert": failure_assert_string
        }
    ))