""" Built in functionality. """
import string
import os
from uuid import uuid4
from random import choices#, randint


def uuid():
    return str(uuid4())


def rand_str(length):
    return "".join(choices(string.ascii_uppercase + string.digits, k=length))


def getenv(input_str, default=None):
    return os.getenv(input_str, default)


def from_response(val, id):
    return 32


def website():
    return "www.stuburl.com/blah"