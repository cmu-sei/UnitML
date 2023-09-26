# UnitML
# Copyright 2023 Carnegie Mellon University.
# NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN "AS-IS" BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.
# Released under a BSD (SEI)-style license, please see license.txt or contact permission@sei.cmu.edu for full terms.
# [DISTRIBUTION STATEMENT A] This material has been approved for public release and unlimited distribution.  Please see Copyright notice for non-US Government use and distribution.
# This Software includes and/or makes use of Third-Party Software each subject to its own license.
# DM23-0976


import json, glob

from unitml.boundary_test_generator import *
from unitml.equivalence_test_generator import *
from unitml.helpers import string_length_adjust

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
        test_file.write(f"# One or more of the descriptor files could not be found.\n")
        test_file.write(f"# Ensure that this directory contains both a Data Pipeline and Trained Model descriptor with the names of the files in the format,\n")
        test_file.write(f"# <Project Name> - Data Pipeline.json and <Project Name> - Trained Model.json.")
        test_file.close()
        return
    except Exception as e:
        test_file = open("test_generated.py", "w")
        test_file.write(f"# Encountered unexpected error when importing descriptor files: {e}")
        test_file.close()
        return

    test_file = open("test_generated.py", "w")

    # Initial setup at the beginning of the file
    test_file.write(f"import pytest\n\n")
    test_file.write(f"from PIL import Image\n")
    test_file.write(f"import glob\n")
    test_file.write(f"import os.path\n\n")

    test_file.write(f"# USER INPUT: Import any modules required for your data pipeline or model\n")
    test_file.write(f"# ex: import tensorflow as tf\n\n")

    test_file.write(f"# USER INPUT: If needed, import your data pipeline and model\n")
    test_file.write(f"# ex: import my_model_file as model\n\n")

    test_file.write(f"# USER INPUT: If needed, specify the file path for the log file that will be written to during failure cases\n")
    test_file.write(f"ex: image_folder_path = logs_folder/log.txt\n")
    test_file.write(f"log_file_path = \"\"\n\n")

    test_file.write(f"# USER INPUT: If needed, specify the folder path that output images will be written to\n")
    test_file.write(f"# ex: image_folder_path = \"images/\"\n")
    test_file.write(f"image_folder_path = \"\"\n\n")

    test_file.write(f"def get_log_file_lines():\n")
    test_file.write(f"\tlog_file = open(log_file_path, \"r\")\n")
    test_file.write(f"\tlines_list = log_file.readlines()\n")
    test_file.write(f"\ttotal_lines = len(lines_list)\n")
    test_file.write(f"\tlog_file.close()\n")
    test_file.write(f"\treturn total_lines\n\n")

    test_file.write(f"def get_last_edited_image():\n")
    test_file.write(f"\tfile_list = glob.glob(image_folder_path + \"*\")\n")
    test_file.write(f"\tlast_edited_image_path = max(file_list, key=os.path.getctime)\n")
    test_file.write(f"\timage = Image.open(last_edited_image_path)\n")
    test_file.write(f"\tformat = last_edited_image_path[-3:]\n")
    test_file.write(f"\treturn image, format\n\n")

    # Defining the DataPipelineInput class
    test_file.write(f"# Defining a class that represents an input into the data pipeline\n")
    test_file.write(f"# NOTE: Input parameters are passed to the data pipeline in the order they\n")
    test_file.write(f"# are saved in the descriptor. If this does not match the order that the Data Pipeline\n")
    test_file.write(f"# is expecting the parameters, edit the order in the descriptor JSON and regenerate this file.")
    test_file.write(f"# ex: data_pipeline_instance.run(test_input.input0, test_input.input1, test_input.input2)")
    test_file.write("class DataPipelineInput:\n")
    test_file.write(f"\tdef __init__(self):\n")
    for item in dp_json["input_spec"]:
        index = dp_json["input_spec"].index(item)
        test_file.write(f"\t\t# Field that relates to the {item['item_name']} item\n")
        test_file.write(f"\t\t# USER INPUT: Define a default vaild value for this item to be used for tests\n")
        test_file.write(f"\t\t# This value will be passed to the model in tests that are not for this item\n")
        if(item["item_type"] == "Integer" or item["item_type"] == "Float"):
            test_file.write(f"\t\tself.input{index} = {item['item_specification']['min_value']}\n\n")
        elif(item["item_type"] == "String"):
            str = string_length_adjust("Test", item['item_specification']["min_length"], item['item_specification']["min_length"])
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
    if tm_json["post_processing"]:
        output_spec = tm_json["final_output_spec"]
    else:
        output_spec = tm_json["output_spec"]

    success_assert_string = generate_success_assert_string(output_spec)

    # Create the string that contains the params for each method
    # test_input.input0, test_input.input1, ...
    param_list = ""
    for item in dp_json["input_spec"]:
        index = dp_json["input_spec"].index(item)
        param_list += f"test_input.input{index}"

        if index < len(dp_json["input_spec"]) - 1:
            param_list += ", "
    
    input_string = f"{param_list}"

    # Generate boundary tests
    test_file.write("# Boundary tests for each data item defined in the data pipeline input specification\n")
    test_file.write("class TestBoundaries:\n")
    for item in dp_json["input_spec"]:
        failure_assert_string = generate_failure_assert_string(item["error_handling"])
        additional_setup_str = ""
        if item["error_handling"]["error_type"] == "Log to file":
            additional_setup_str = f"\t\tlines_before_test = get_log_file_lines()\n"

        if item["item_type"] == "Integer":
            generate_integer_boundary_tests(test_file, item, dp_json["input_spec"].index(item), input_string, additional_setup_str, success_assert_string, failure_assert_string)
        elif item["item_type"] == "Float":
            generate_float_boundary_tests(test_file, item, dp_json["input_spec"].index(item), input_string, additional_setup_str, success_assert_string, failure_assert_string)
        elif item["item_type"] == "String":
            generate_string_boundary_tests(test_file, item, dp_json["input_spec"].index(item), input_string, additional_setup_str, success_assert_string, failure_assert_string)
        elif item["item_type"] == "Image":
            generate_image_boundary_tests(test_file, item, dp_json["input_spec"].index(item), input_string, additional_setup_str, success_assert_string, failure_assert_string)
        elif item["item_type"] == "Other":
            test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")
            test_file.write(f"\t# Cannot generate boundary tests for items of type \"Other\"\n\n")
        else:
            test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")
            test_file.write(f"\t# Cannot generate boundary tests for items without a type specified in descriptor.\n\n")

    # Generate equivalence tests
    test_file.write("# Equivalence class tests for each data item defined in the data pipeline input specification\n")
    test_file.write("class TestEquivalenceClass:\n")
    for item in dp_json["input_spec"]:
        failure_assert_string = generate_failure_assert_string(item["error_handling"])
        additional_setup_str = ""
        if item["error_handling"]["error_type"] == "Log to file":
            additional_setup_str = f"\t\tlines_before_test = get_log_file_lines()\n"

        if item["item_type"] == "Integer":
            generate_integer_equivalence_tests(test_file, item, dp_json["input_spec"].index(item), input_string, additional_setup_str, success_assert_string, failure_assert_string)
        elif item["item_type"] == "Float":
            generate_float_equivalence_tests(test_file, item, dp_json["input_spec"].index(item), input_string, additional_setup_str, success_assert_string, failure_assert_string)
        elif item["item_type"] == "String":
            generate_string_equivalence_tests(test_file, item, dp_json["input_spec"].index(item), input_string, additional_setup_str, success_assert_string, failure_assert_string)            
        elif item["item_type"] == "Image":
            generate_image_equivalence_tests(test_file, item, dp_json["input_spec"].index(item), input_string, additional_setup_str, success_assert_string, failure_assert_string)            
        elif item["item_type"] == "Other":
            test_file.write(f"\t# Testing the equivalence classes of {item['item_name']}\n")
            test_file.write(f"\t# Cannot generate equivalence tests for items of type \"Other\"\n\n")
        else:
            test_file.write(f"\t# Testing the equivalence classes of {item['item_name']}\n")
            test_file.write(f"\t# Cannot generate boundary tests for items without a type specified in descriptor.\n\n")

    test_file.close()

    return "Tests created."


def generate_success_assert_string(output_spec) -> str:
    assert_string = ""
    if any(output["item_type"] == "Image" for output in output_spec):
        assert_string += f"\t\toutput_image = get_last_edited_image()\n"

    assert_string += f"\t\tassert (\n\t\t\t"

    for output in output_spec:
        index = output_spec.index(output)

        if output["item_type"] in ["Integer", "Float"]:
            assert_string += f"(model_output[{index}] >= {output['item_specification']['min_value']} and model_output[{index}] <= {output['item_specification']['max_value']})"
        elif output["item_type"] == "String":
            assert_string += f"(len(model_output[{index}]) >= {output['item_specification']['min_length']} and len(model_output[{index}]) <= {output['item_specification']['max_length']})"
        elif output["item_type"] == "Image":
            assert_string += f"(output_image[0].size == ({output['item_specification']['resolution_x']}, {output['item_specification']['resolution_y']}) and output_image[1] == \"{output['item_specification']['image_format'].lower()}\")"
        elif output["item_type"] == "Other":
            assert_string += f"(True) # Cannot generate an assert check for an error output of type \"Other\""
        else:
            assert_string += f"False # No item type specified in descriptor"

        if index < len(output_spec) - 1:
            assert_string += f"\n\t\t\tand "
        else:
            assert_string += f"\n\t\t)\n\n"

    return assert_string


def generate_failure_assert_string(error_handling) -> str:
    if error_handling["error_type"] == "Return none":
        return f"\t\tassert model_output == None\n\n"
    elif error_handling["error_type"] == "Return error code":
        return f"\t\tassert model_output == {error_handling['error_code_value']}\n\n"
    elif error_handling["error_type"] == "Log to console":
        return f"\t\tassert False # Error output should have logged to console during model execution. Check test output to confirm.\n\n"
    elif error_handling["error_type"] == "Log to file":
        return f"\t\tassert lines_before_test < get_log_file_lines()\n\n"
    elif error_handling["error_type"] == "Other":
        return f"\t\tassert False # Cannot generate an assert statement for an error output of type \"Other\"\n\n"
    else:
        return f"\t\t # assert False # No error type specified in descriptor.\n\n"