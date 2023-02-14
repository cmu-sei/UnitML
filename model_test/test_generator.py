import json
import glob

def generate_test_file():
    # Importing the descriptors
    dp_file = open(glob.glob('* - Data Pipeline.json')[0], "r")
    dp_json = json.load(dp_file)
    dp_file.close()

    tm_file = open(glob.glob('* - Trained Model.json')[0], "r")
    tm_json = json.load(tm_file)
    tm_file.close()

    test_file = open("test_generated.py", "w")

    # Declare any inputs/outputs with or without descriptor data
    # test_file.write("# Set input params\n")
    # test_file.write("max_input = " + str(dp_json["version"]) + "\n")
    # test_file.write("min_input = " + str(tm_json["version"]) + "\n\n")

    # Initial setup at the beginning of the file
    test_file.write("# Import any required modules\n")
    test_file.write("# ex: import tensorflow as tf\n\n")

    test_file.write("# Import your data pipeline and model\n")
    test_file.write("# ex: \n\n")

    test_file.write("# Define a class for an input into your data pipeline")

    test_file.write("# Define a class for your data pipeline here\n")
    test_file.write("class DataPipeline:\n")
    test_file.write("\tdef __init__(self):\n")
    test_file.write("\t\tpass\n\n")
    test_file.write("\tdef run(self, input):\n")
    test_file.write("\t\treturn input\n\n")

    test_file.write("# Define your model here\n")
    test_file.write("class Model:\n")
    test_file.write("\tdef __init__(self):\n")
    test_file.write("\t\t# Define how to load your model\n")
    test_file.write("\t\t# ex: self.model = tf.keras.models.load_model(\"my_model_directory\")\n")
    test_file.write("\t\tself.model = \n\n")
    test_file.write("\tdef run(self, input):\n")
    test_file.write("\t\treturn input\n\n")

    test_file.write("# Initialize an instance of your data pipeline\n")
    test_file.write("test_data_pipeline = DataPipeline()\n\n")

    test_file.write("# Initialize an instance of your model\n")
    test_file.write("test_model = Model()\n\n\n")

    # Generate and add boundary tests to the file
    test_file.write("class TestBoundaries:\n")
    for item in dp_json['input_spec']:
        if item['item_type'] == "Integer":
            generate_integer_boundary_tests(test_file, item, dp_json['input_spec'].index(item))

    test_file.close()

    return "Tests created."

def generate_integer_boundary_tests(test_file, item, item_index):
    test_file.write(f"\t# Testing the boundaries of {item['item_name']}\n")
    test_file.write(f"\tdef test_boundary_{item_index}_{0}(self):\n")
    test_file.write(f"\t\tdata_pipeline_input = [{item['min_value'] - 1}, ..., ...]\n")
    test_file.write(f"\t\tdata_pipeline_output = test_data_pipeline.run(data_pipeline_input)\n")
    test_file.write(f"\t\tassert test_model.run(data_pipeline_output) == {item_index}\n\n")

    test_file.write(f"\tdef test_boundary_{item_index}_{1}(self):\n")
    test_file.write(f"\t\tdata_pipeline_input = [{item['min_value']}, ..., ...]\n")
    test_file.write(f"\t\tdata_pipeline_output = test_data_pipeline.run(data_pipeline_input)\n")
    test_file.write(f"\t\tassert test_model.run(data_pipeline_output) == {item_index}\n\n")

    test_file.write(f"\tdef test_boundary_{item_index}_{0}(self):\n")
    test_file.write(f"\t\tdata_pipeline_input = [{item['min_value'] + 1}, ..., ...]\n")
    test_file.write(f"\t\tdata_pipeline_output = test_data_pipeline.run(data_pipeline_input)\n")
    test_file.write(f"\t\tassert test_model.run(data_pipeline_output) == {item_index}\n\n")