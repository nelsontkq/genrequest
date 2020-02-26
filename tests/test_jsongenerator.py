from genrequest import Generator
import time
import os


def test_parse_variables_doesnt_lose_type():
    gen = Generator()
    assert gen.parse_variables("10")[0][0] == 10
    assert gen.parse_variables("'10'")[0][0] == "10"
    assert gen.parse_variables("False")[0][0] == False
    assert gen.parse_variables("True")[0][0] == True
    assert gen.parse_variables("13.41")[0][0] == 13.41
    assert gen.parse_variables("key='24'")[1]["key"] == "24"
    assert gen.parse_variables("key=24")[1]["key"] == 24
    assert gen.parse_variables("key=False")[1]["key"] == False
    assert gen.parse_variables("key=True")[1]["key"] == True
    assert gen.parse_variables("key=13.42")[1]["key"] == 13.42


def test_parse_function_generates_different_every_time():
    gen = Generator()
    func = gen._parse_function("{{address()}}")
    assert func() != func()
    func = gen._parse_function("{{random_string(4)}}")
    assert func() != func()


def test_generate():
    os.environ["ENDPOINT"] = "www.endpoint.com"
    os.environ["CUSTOMER"] = "Customer1"
    gen = Generator()
    with open("tests/item-update-removes-alt-units.yaml") as yaml:
        gen.load_template(yaml.read())
    _ = [gen.generate() for f in range(3)]


def test_generates_quick_enough():
    """ Should never take longer than ~100ms per body."""
    then = time.time()
    gen = Generator()
    k = 20
    with open("tests/item-update-removes-alt-units.yaml") as yaml:
        gen.load_template(yaml.read())
    _ = [gen.generate() for f in range(k)]
    now = time.time()

    print(f"{now - then} seconds average for 20")
    assert now - then < k / 10
