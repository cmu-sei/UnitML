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
    test_file.write(f"\t# Testing the equivalence classes of {item['item_name']}\n")
    test_file.write("\t# Tests outside classes that are expected to fail\n")
    test_file.write("\t@pytest.mark.xfail\n")
    test_file.write(equivalence_test_template.substitute(
        {
            "equivalence_list": f"["
                "\"\""
            "]",
            "item_index": item_index,
            "test_index": 1,
            "input_string": input_string,
            "assert": failure_assert_string
        }
    ))


def generate_image_equivalence_tests():
    pass