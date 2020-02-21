import re
import json
import inspect
from enum import Enum
from ruamel import yaml
import jsonfunctions
# import dicttoxml
import json


class FunctionRunner:
    def __init__(self, function, variables):
        self._function = function
        if variables:
            self._args, self._kwargs = variables
        else:
            self._args = []
            self._kwargs = {}

    def __str__(self):
        res = self._function(*self._args, **self._kwargs)
        if res is None:
            raise ValueError(
                f"None was returned from function '{self._function.__name__}' with args {self._args} and kwargs {self._kwargs}."
            )
        return str(res)


class OutputType(Enum):
    YAML = 0
    JSON = 1
    DICT = 2
    # XML = 3


class TagReplacer:
    def _set_functions(self, custom_functions=None):
        if custom_functions:
            if not isinstance(custom_functions, list):
                raise ValueError("custom_functions should be a list of functions!")
            for func in custom_functions:
                self.add_function(func)
        for _, func in inspect.getmembers(jsonfunctions, inspect.isfunction):
            self.add_function(func)

    def _convert_to_target_type(self, unconverted: dict, output_type=None):
        output_type = output_type or self.output_type
        if output_type == OutputType.JSON:
            return json.dumps(unconverted)
        elif output_type == OutputType.DICT:
            return unconverted
        elif output_type == OutputType.YAML:
            return yaml.dump(unconverted)
        # elif self.output_type == OutputType.XML:
        #     return dicttoxml.dicttoxml(unconverted, custom_root="template")

    @property
    def output_type(self):
        """ The output type.
        """
        return self._output_type

    @output_type.setter
    def set_output(self, value: OutputType):
        self._output_type = value

    @property
    def functions(self):
        """ A dictionary of [function_name] = function
        """
        return self._functions

    def __init__(self, custom_functions=None, read_format="yaml", write_format="json", output_type=OutputType.JSON):
        self._write_format = write_format
        self._output_type = output_type
        self._read_format = read_format
        self._functions = {}
        self._template = []
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

    def _parse_function(self, input_str: str):
        left, right = re.search(r"{{\s*(\w+)\((.*?)\)", input_str).groups()
        variables = self.parse_variables(right)
        if left not in self._functions:
            raise ValueError(f"A function called {left} was not defined!")
        return FunctionRunner(self._functions[left], variables)

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
            elif "=" in val:
                split = list(map(str.strip, val.split("=")))
                key_vals[split[0]] = parse_sub(split[1])
                return None
            elif val == "True" or val == "False":
                return val == "True"
            try:
                return int(val)
            except ValueError:
                try:
                    return float(val)
                except ValueError:
                    raise ValueError(f"{val} is not a primitive type!")

        if input_str:
            for val in map(str.strip, input_str.split(",")):
                result = parse_sub(val)
                if result is not None:
                    output.append(result)
            return output, key_vals

    def load_template(self, input_str: str):
        """ Load a template into an array for easy generation of multiple requests.
        """
        for item in re.split(r"({{.*?}})", input_str):
            if item.startswith("{{") and "(" in item:
                self._template.append(self._parse_function(item))
            else:
                self._template.append(item)

    def generate(self, k=1, with_variables=True, output_type=None):
        """ Generate k json bodies using the provided template
        """
        results = []
        for _ in range(k):
            result = "".join(map(str, self._template))
            if with_variables:
                body = yaml.load(result, Loader=yaml.Loader)
                variables = body.get("variables", {})
                if variables:
                    result = re.sub(
                        r"{{(\w+)}}",
                        lambda m: variables.get(m.group(1), m.group(0)),
                        result,
                    )
            results.append(self._convert_to_target_type(yaml.load(result, Loader=yaml.Loader), output_type))
        return results


class JsonGenerator:
    def __init__(self, custom_functions=None, **kwargs):

        pass


def create_generator(input_json) -> JsonGenerator:
    pass

