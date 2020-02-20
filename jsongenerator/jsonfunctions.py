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
    os.getenv(input_str, default)
