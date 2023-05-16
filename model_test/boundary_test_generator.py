import string, random

from string import Template


boundary_test_template = Template(
    "\t@pytest.mark.parametrize(\"boundary_value\", ${boundary_list})\n"
    "\tdef test_boundary_${item_index}(self, boundary_value):\n"
    "\t\ttest_input = DataPipelineInput()\n"
    "\t\ttest_input.input${item_index} = boundary_value\n"
    "\t\tdata_pipeline_output = data_pipeline_instance.run(${input_string})\n"
    "\t\tmodel_output = model_instance.run(data_pipeline_output)\n"
    "\t\t${assert}\n\n"
)


def generate_integer_boundary_tests(test_file, item, item_index, input_string, assert_string):
    test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")
    
    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"{item['min_value'] - 1}, "
                f"{item['min_value']}, "
                f"{item['min_value'] + 1}, "
                f"{item['max_value'] - 1}, "
                f"{item['max_value']}, "
                f"{item['max_value'] + 1}"
            "]",
            "item_index": item_index, 
            "input_string": input_string,
            "assert": assert_string
        }
    ))


def generate_float_boundary_tests(test_file, item, item_index, input_string, assert_string):
    test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")

    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"{item['min_value'] - .01:.2f}, "
                f"{item['min_value']:.2f}, "
                f"{item['min_value'] + .01:.2f}, "
                f"{item['max_value'] - .01:.2f}, "
                f"{item['max_value']:.2f}, "
                f"{item['max_value'] + .01:.2f}"
            "]",
            "item_index": item_index,
            "input_string": input_string,
            "assert": assert_string
        }
    ))


def generate_string_boundary_tests(test_file, item, item_index, input_string, assert_string):
    test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")
    
    random_str = ''.join(random.choice(string.ascii_letters) for i in range(item['max_length'] + 1))

    test_file.write(boundary_test_template.substitute(
        {
            "boundary_list": f"["
                f"\"{random_str[:item['min_length'] - 1]}\", "
                f"\"{random_str[:item['min_length']]}\", "
                f"\"{random_str[:item['min_length'] + 1]}\", "
                f"\"{random_str[:item['max_length'] - 1]}\", "
                f"\"{random_str[:item['max_length']]}\", "
                f"\"{random_str[:item['max_length'] + 1]}\""
            "]",
            "item_index": item_index, 
            "input_string": input_string,
            "assert": assert_string
        }
    ))


def generate_image_boundary_tests():
    pass