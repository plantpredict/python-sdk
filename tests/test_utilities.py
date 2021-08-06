import unittest
import json

from plantpredict import utilities


class TestUtilities(unittest.TestCase):

    def test_decorate_all_methods(self):
        # test that decorating a class with a function that adds 1 to the output results in each method (which returns
        # the sum of two numbers) returns a number 1 greater than it would un-decorated
        def add_one_to_output(function):
            def function_wrapper(*args, **kwargs):
                number = function(*args, **kwargs)
                return number + 1

            return function_wrapper

        @utilities.decorate_all_methods(add_one_to_output)
        class TestDecorateAllMethods(object):
            def add_two(self):
                return self.number + 2

            def add_three(self):
                return self.number + 3

            def add_four(self):
                return self.number + 4

            def __init__(self):
                self.number = 100

        tester = TestDecorateAllMethods()
        self.assertEqual(tester.add_two(), 103)
        self.assertEqual(tester.add_three(), 104)
        self.assertEqual(tester.add_four(), 105)

    def test_camel_to_snake(self):
        camel_key = "thisIsOnlyATest"
        snake_key = utilities.camel_to_snake(camel_key)
        self.assertEqual(snake_key, "this_is_only_a_test")

    def test_camel_to_snake_one_word(self):
        camel_key = "test"
        snake_key = utilities.camel_to_snake(camel_key)
        self.assertEqual(snake_key, "test")

    def test_snake_to_camel(self):
        snake_key = "this_is_only_a_test"
        camel_key = utilities.snake_to_camel(snake_key)
        self.assertEqual(camel_key, "thisIsOnlyATest")

    def test_snake_to_camel_one_word(self):
        snake_key = "test"
        camel_key = utilities.snake_to_camel(snake_key)
        self.assertEqual(camel_key, "test")

    def test_convert_json_camel_to_snake(self):
        with open('test_data/test_convert_json_camel.json', 'rb') as json_file:
            snake_dict = utilities.convert_json(json.load(json_file), utilities.camel_to_snake)

        with open('test_data/test_convert_json_snake.json', 'rb') as json_file:
            self.assertEqual(snake_dict, json.load(json_file))

    def test_convert_json_list_camel_to_snake(self):
        camel_list = [{"firstItem": 1}, {"secondItem": 2}, {"thirdItem": 3}]
        snake_list = utilities.convert_json_list(camel_list, utilities.camel_to_snake)
        self.assertEqual(snake_list, [{"first_item": 1}, {"second_item": 2}, {"third_item": 3}])

    def test_convert_json_list_snake_to_camel(self):
        snake_list = [{"first_item": 1}, {"second_item": 2}, {"third_item": 3}]
        camel_list = utilities.convert_json_list(snake_list, utilities.snake_to_camel)
        self.assertEqual(camel_list, [{"firstItem": 1}, {"secondItem": 2}, {"thirdItem": 3}])


if __name__ == '__main__':
    unittest.main()