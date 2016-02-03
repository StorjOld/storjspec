import json
import unittest
import jsonschema


class TestContract(unittest.TestCase):

    def test_valid_example(self):
        with open("schema.json", 'r') as schema_file:
            schema = json.loads(schema_file.read())
        with open("example.json", 'r') as example_file:
            example = json.loads(example_file.read())
        jsonschema.validate(example, schema)

    # TODO test edge cases and invalid contracts


if __name__ == "__main__":
    unittest.main()
