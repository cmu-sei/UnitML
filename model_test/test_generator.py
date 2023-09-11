import json, glob

from model_test.boundary_test_generator import *
from model_test.equivalence_test_generator import *

def generate_test_file():
    # Importing the descriptors
    try: 
        dp_file = open(glob.glob('* - Data Pipeline.json')[0], "r")
        dp_json = json.load(dp_file)
        dp_file.close()

        tm_file = open(glob.glob('* - Trained Model.json')[0], "r")
        tm_json = json.load(tm_file)
        tm_file.close()
    except IndexError as e:
        test_file = open("test_generated.py", "w")
        test_file.write("# One or more of the descriptor files could not be found.\n")
        test_file.write("# Ensure that this directory contains both a Data Pipeline and Trained Model descriptor with the names of the files in the format,\n")
        test_file.write("# <Project Name> - Data Pipeline.json and <Project Name> - Trained Model.json.")
        test_file.close()
        return
    except Exception as e:
        test_file = open("test_generated.py", "w")
        test_file.write(f"# Encountered unexpected error when importing descriptor files: {e}")
        test_file.close()
        return

    test_file = open("test_generated.py", "w")

    # Initial setup at the beginning of the file
    test_file.write("import numpy as np\n")
    test_file.write("import pytest\n\n")
    test_file.write("from PIL import Image\n\n")
    test_file.write("# USER INPUT: Import any modules required for your data pipeline or model\n")
    test_file.write("# ex: import tensorflow as tf\n\n")

    test_file.write("# USER INPUT: If needed, import your data pipeline and model\n")
    test_file.write("# ex: import my_model_file as model\n\n")

    test_file.write(f"# USER INPUT: If needed, specify the file path for the log file that will be written to\n")
    test_file.write(f"log_file_path = \"\"\n\n")

    test_file.write(f"def assert_log_file():\n")
    test_file.write(f"\treturn true\n\n")

    # Defining the DataPipelineInput class
    test_file.write("# Defining a class that represents an input into the data pipeline\n")
    test_file.write("class DataPipelineInput:\n")
    test_file.write(f"\tdef __init__(self):\n")
    for item in dp_json["input_spec"]:
        index = dp_json["input_spec"].index(item)
        test_file.write(f"\t\t# Field that relates to the {item['item_name']} item\n")
        test_file.write(f"\t\t# USER INPUT: Define a default vaild value for this item to be used for tests\n")
        test_file.write(f"\t\t# This value will be passed to the model in tests that are not for this item")
        if(item["item_type"] == "Integer" or item["item_type"] == "Float"):
            test_file.write(f"\t\tself.input{index} = {item['min_value']}\n\n")
        elif(item["item_type"] == "String"):
            str = string_length_adjust("Test", item["min_length"], item["min_length"])
            test_file.write(f"\t\tself.input{index} = \"{str}\"\n\n")
        else:
            test_file.write(f"\t\tself.input{index} = None \n\n")


    # Defining the DataPipeline class
    test_file.write("# Defining a class for your data pipeline here\n")
    test_file.write("class DataPipeline:\n")
    test_file.write("\t# USER INPUT: Define any setup that is needed to instantiate your data pipeline\n")
    test_file.write("\tdef __init__(self):\n")
    test_file.write("\t\tpass\n\n")
    test_file.write("\t# USER INPUT: Define how to run your data pipeline. The run method accepts an instance of the\n")
    test_file.write("\t# DataPipelineInput class and it should return an object that is ready to be passed to the model\n")
    test_file.write("\tdef run(self, input: DataPipelineInput):\n")
    test_file.write("\t\treturn input\n\n")

    # Defining the model class
    test_file.write("# Define your model here\n")
    test_file.write("class Model:\n")
    test_file.write("\t# USER INPUT: Define how to load your model\n")
    test_file.write("\t# ex: self.model = pickle.load(open('model.sav', 'rb'))\n")
    test_file.write("\tdef __init__(self):\n")
    test_file.write("\t\tself.model = \n\n")
    test_file.write("\t# USER INPUT: Define how to run your model. The input parameter will be the direct output from DataPipeline.run\n")
    test_file.write("\t# Model outputs will be accessed under the assumption that the output is packaged as a tuple, this function must return output in that format.\n")
    test_file.write("\t# ex:\n")
    test_file.write("\t# return_value1, return_value2 = self.model.predict(input)\n")
    test_file.write("\t# return return_value1, return_value2\n")
    test_file.write("\tdef run(self, input):\n")
    test_file.write("\t\treturn input\n\n")

    test_file.write("# Initializing an instance of the data pipeline to be used for tests\n")
    test_file.write("data_pipeline_instance = DataPipeline()\n\n")

    test_file.write("# Initializing an instance of the model to be used for tests\n")
    test_file.write("model_instance = Model()\n\n\n")

    # Expected output for assertions based on trained model output/final output spec
    output_spec = {}
    if tm_json['post_processing']:
        output_spec = tm_json['final_output_spec']
    else:
        output_spec = tm_json['output_spec']

    success_assert_string = generate_success_assert_string(output_spec)
    failure_assert_string = generate_failure_assert_string(output_spec)
        
    # Generate boundary tests
    param_list = ""
    for item in dp_json["input_spec"]:
        index = dp_json["input_spec"].index(item)
        param_list += f"test_input.input{index}"

        if index < len(dp_json["input_spec"]) - 1:
            param_list += ", "
    
    input_string = f"{param_list}"

    test_file.write("# Boundary tests for each data item defined in the data pipeline input specification\n")
    test_file.write("class TestBoundaries:\n")
    for item in dp_json["input_spec"]:
        if item["item_type"] == "Integer":
            generate_integer_boundary_tests(test_file, item, dp_json["input_spec"].index(item), input_string, success_assert_string, failure_assert_string)
        elif item["item_type"] == "Float":
            generate_float_boundary_tests(test_file, item, dp_json["input_spec"].index(item), input_string, success_assert_string, failure_assert_string)
        elif item["item_type"] == "String":
            generate_string_boundary_tests(test_file, item, dp_json["input_spec"].index(item), input_string, success_assert_string, failure_assert_string)
        elif item["item_type"] == "Image":
            generate_image_boundary_tests(test_file, item, dp_json["input_spec"].index(item), input_string, success_assert_string, failure_assert_string)
        

    test_file.write("# Equivalence class tests for each data item defined in the data pipeline input specification\n")
    test_file.write("class TestEquivalenceClass:\n")
    for item in dp_json["input_spec"]:
        if item["item_type"] == "Integer":
            generate_integer_equivalence_tests(test_file, item, dp_json["input_spec"].index(item), input_string, success_assert_string, failure_assert_string)
        elif item["item_type"] == "Float":
            pass
        elif item["item_type"] == "String":
            generate_string_equivalence_tests(test_file, item, dp_json["input_spec"].index(item), input_string, success_assert_string, failure_assert_string)            
        elif item["item_type"] == "Image":
            pass

    test_file.close()

    return "Tests created."


def generate_success_assert_string(output_spec) -> str:
    assert_string = "\t\tassert (\n\t\t\t"

    for item in output_spec:
        index = output_spec.index(item)

        if item["item_type"] in ["Integer", "Float"]:
            assert_string += f"(model_output[{index}] >= {item['min_value']} and model_output[{index}] <= {item['max_value']})"
        elif item["item_type"] == "String":
            assert_string += f"(len(model_output[{index}]) >= {item['min_length']} and len(model_output[{index}]) <= {item['max_length']})"
        elif item["item_type"] == "Image":
            assert_string += f"(model_output[{index}].size[0] == {item['resolution_x']} and model_output[{index}].size[1] == {item['resolution_y']})"

        if index < len(output_spec) - 1:
            assert_string += "\n\t\t\tand "
        else:
            assert_string += "\n\t\t)\n\n"

    return assert_string


def generate_failure_assert_string(output_spec) -> str:
    assert_string = ("\t\t# USER INPUT: Define failure case\n"
                    "\t\tassert False\n\n")

    return assert_string