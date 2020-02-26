import re
import json
import inspect
from faker import Faker
from enum import Enum
from ruamel import yaml
from string import ascii_uppercase, digits
import os
from uuid import uuid4
from faker.providers import BaseProvider
import functools
import json


class GeneratorProvider(BaseProvider):
    def getenv(self, input_str, default=None):
        return os.getenv(input_str, default)

    def random_string(self, length):
        return "".join(
            self.random_choices(elements=tuple(
                ascii_uppercase + digits), length=length)
        )


class OutputType(Enum):
    YAML = 0
    JSON = 1
    DICT = 2
    # XML = 3


class Generator:
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

    def __init__(
        self, custom_generator=None, output_type=OutputType.JSON
    ):
        self._output_type = output_type
        self._template = []
        self._fake = Faker()
        self._fake.add_provider(GeneratorProvider)
        if custom_generator:
            if isinstance(custom_generator, list):
                for i in custom_generator:
                    self._fake.add_provider(i)
            else:
                self._fake.add_provider(custom_generator)

    def _parse_function(self, input_str: str):
        left, right = re.search(r"{{\s*(\w+)\((.*?)\)", input_str).groups()

        func = getattr(self._fake, left)
        if not func:
            raise ValueError(
                f"A function called {left} was not defined in provider!")
        if right:
            arr, dic = self.parse_variables(right)
            return functools.partial(func, *arr, **dic)
        return func

    @classmethod
    def parse_variables(cls, input_str: str):
        """ Parse the variables provided to the method in the json. """
        output = []
        key_vals = {}

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
        self._template = []
        for item in re.split(r"({{.*?}})", input_str):
            if item.startswith("{{") and "(" in item:
                self._template.append(self._parse_function(item))
            else:
                self._template.append(item)

    def _handle_record(self, item):
        if callable(item):
            return str(item())
        return str(item)

    def generate(self, k=1, with_variables=True, output_type=None):
        """ Generate k json bodies using the provided template
        """
        for _ in range(k):

            result = "".join(map(self._handle_record, self._template))
            if with_variables:
                body = yaml.load(result, Loader=yaml.Loader)
                variables = body.get("variables", {})
                if variables:
                    result = re.sub(
                        r"{{(\w+)}}",
                        lambda m: variables.get(m.group(1), m.group(0)),
                        result,
                    )
            yield self._convert_to_target_type(
                yaml.load(result, Loader=yaml.Loader).get(
                    "template"), output_type
            )
