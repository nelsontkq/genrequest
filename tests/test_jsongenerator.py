from jsongenerator.jsongenerator import Generator
import time
import os


def test_parse_variables_doesnt_lose_type():
    x = Generator()
    assert x.parse_variables("10")[0][0] == 10
    assert x.parse_variables("'10'")[0][0] == '10'
    assert x.parse_variables("False")[0][0] == False
    assert x.parse_variables("True")[0][0] == True
    assert x.parse_variables("13.41")[0][0] == 13.41
    assert x.parse_variables("key='24'")[1]['key'] == '24'
    assert x.parse_variables("key=24")[1]['key'] == 24
    assert x.parse_variables("key=False")[1]['key'] == False
    assert x.parse_variables("key=True")[1]['key'] == True
    assert x.parse_variables("key=13.42")[1]['key'] == 13.42

def test_parse_function_generates_different_every_time():
    x = Generator()
    func = x._parse_function("{{address()}}")
    assert func() != func()


def test_generate():
    os.environ["ENDPOINT"] = "www.endpoint.com"
    os.environ["CUSTOMER"] = "Customer1"
    x = Generator()
    with open("tests/item-update-removes-alt-units.yaml") as yaml:
        x.load_template(yaml.read())
    results = x.generate(k=3)
    for result in results:
        pass


def test_generates_quick_enough():
    """ Should never take longer than ~100ms per body."""
    then = time.time()
    x = Generator()
    k = 20
    with open("tests/item-update-removes-alt-units.yaml") as yaml:
        x.load_template(yaml.read())
    for result in x.generate(k=k):
        pass
    now = time.time()

    assert now - then < k / 10

