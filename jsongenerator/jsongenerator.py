import re
import json
import inspect
import jsonfunctions
import ruamel.yaml
import json

class Runnable:
    def __init__(self, function, variables):
        self._function = function
        self._args, self._kwargs = variables
    
    def __repr__(self):
        return self._function(*self._args, **self._kwargs)


class TagReplacer:
    def _set_functions(self, custom_functions=None):
        if custom_functions:
            if not isinstance(custom_functions, list):
                raise ValueError("custom_functions should be a list of functions!")
            for func in custom_functions:
                self.add_function(func)
        for _, func in inspect.getmembers(jsonfunctions, inspect.isfunction):
            self.add_function(func)

    @property
    def functions(self):
        """ A dictionary of [function_name] = function
        """
        return self._functions

    def __init__(self, custom_functions=None, read_format="yaml", write_format="json"):
        self._write_format = write_format
        self._functions = {}
        self._set_functions(custom_functions)

    def pop_function(self, value):
        if value in self._functions:
            return self._functions.pop(value)

    def add_function(self, value):
        if not callable(value):
            raise ValueError(f"Functions must be callable! provided: {value}")
        if value.__name__ in self._functions:
            raise ValueError(f"A function called {value.__name__} is already defined!")
        self._functions[value.__name__] = value

    def parse_function(self, input_str: str):
        left, right = input_str.split("(")
        variables = self.parse_variables(right[:-1])
        if left not in self._functions:
            raise ValueError(f"A function called {left} was not defined!")
        return Runnable(self._functions[left], variables)

    @classmethod
    def parse_variables(cls, input_str: str):
        """ Parse the variables provided to the method in the json. """
        output = []
        key_vals = {}
        template = []

        def parse_sub(val):
            if (
                val.startswith("'")
                and val.endswith("'")
                or val.startswith('"')
                and val.endswith('"')
            ):
                return val[1:-1]
            if "=" in val:
                split = list(map(str.strip, val.split("=")))
                key_vals[split[0]] = parse_sub(split[1])
                return None
            try:
                return int(val)
            except ValueError:
                return float(val)

        for val in map(str.strip, input_str.split(",")):
            result = parse_sub(val)
            if result is not None:
                output.append(result)
        return output, key_vals

    def load_template(self, input_str: str):
        """ Load a template into an array for easy generation of multiple requests.
        """
        if self._write_format == "json" and self._read_format == "yaml":
            yaml = ruamel.yaml.YAML()
            yaml.explicit_start = True
            data = yaml.load(input_str)
            input_str = json.dump(data)
        output = []
        function_start = False
        function_end = False
        for item in re.split(r"({{\s*|\s*}})", input_str):
            if function_end:
                function_end = False
            elif captured:
                output.append(self.parse_function(item))
                function_end = True
            elif item.startswith("{{"):
                function_start = True
            else:
                output.append(item)
        self._template = output

    def generate(self, k=1):
        """ Generate k json bodies using the provided template
        """
        return "".join(self._template)


    # def replace_from_response(self, left, responses_dict):

    #     if not isinstance(left, str):
    #         left = json.dumps(left)
    #     if isinstance(right, str):
    #         right = json.loads(right)

    #     def callback(matchobj):
    #         key = matchobj.group(1)
    #         try:
    #             value = responses_dict[key]
    #         except KeyError:
    #             raise ValueError(
    #                 f"request: {key} has not been made yet! properties must be in chronological order"
    #             )
    #         return jmespath.search(value, matchobj.group(2))

    #     left = re.sub(r"{{(\w+)\|(.*)}}", callback, left)
    #     return json.loads(left)


class JsonGenerator:
    def __init__(self, custom_functions=None, **kwargs):

        pass


def create_generator(input_json) -> JsonGenerator:
    pass

